<!-- src/lib/components/common/ErrorBoundary.svelte -->
<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { browser } from '$app/environment';
  import toast from 'svelte-french-toast';
  import Button from './Button.svelte';
  import Card from './Card.svelte';
  
  let {
    fallback = null,
    onError = null,
    showDetails = false,
    showReload = true,
    customMessage = '',
    children,
    ...restProps
  } = $props();
  
  const dispatch = createEventDispatcher();
  
  let hasError = $state(false);
  let error = $state(null);
  let errorInfo = $state(null);
  let componentStack = $state('');
  
  // Global error handler
  onMount(() => {
    if (browser) {
      const originalOnError = window.onerror;
      const originalOnUnhandledRejection = window.onunhandledrejection;
      
      // Handle JavaScript errors
      window.onerror = (message, source, lineno, colno, error) => {
        handleError(error || new Error(message), {
          source,
          line: lineno,
          column: colno,
          type: 'javascript'
        });
        
        if (originalOnError) {
          return originalOnError(message, source, lineno, colno, error);
        }
      };
      
      // Handle unhandled promise rejections
      window.onunhandledrejection = (event) => {
        handleError(event.reason, {
          type: 'unhandled-promise',
          promise: event.promise
        });
        
        if (originalOnUnhandledRejection) {
          return originalOnUnhandledRejection(event);
        }
      };
      
      // Cleanup on component destroy
      return () => {
        window.onerror = originalOnError;
        window.onunhandledrejection = originalOnUnhandledRejection;
      };
    }
  });
  
  function handleError(err, info = {}) {
    hasError = true;
    error = err;
    errorInfo = info;
    
    // Create component stack trace
    componentStack = generateComponentStack(err);
    
    // Log error for debugging
    console.error('Error boundary caught an error:', {
      error: err,
      info: info,
      componentStack: componentStack,
      userAgent: navigator.userAgent,
      url: window.location.href,
      timestamp: new Date().toISOString()
    });
    
    // Call custom error handler if provided
    if (onError) {
      try {
        onError(err, info);
      } catch (handlerError) {
        console.error('Error in custom error handler:', handlerError);
      }
    }
    
    // Dispatch error event
    dispatch('error', {
      error: err,
      info: info,
      componentStack: componentStack
    });
    
    // Show toast notification
    if (browser) {
      const errorMessage = err?.message || 'An unexpected error occurred';
      toast.error(`Error: ${errorMessage}`, {
        duration: 5000
      });
    }
  }
  
  function generateComponentStack(err) {
    if (!err || !err.stack) return 'No stack trace available';
    
    // Try to extract component information from stack trace
    const stack = err.stack;
    const lines = stack.split('\n');
    const componentLines = lines.filter(line => 
      line.includes('.svelte') || 
      line.includes('src/lib/components') ||
      line.includes('src/routes')
    );
    
    return componentLines.slice(0, 5).join('\n');
  }
  
  function retry() {
    hasError = false;
    error = null;
    errorInfo = null;
    componentStack = '';
    
    dispatch('retry');
  }
  
  function reload() {
    if (browser) {
      window.location.reload();
    }
  }
  
  function reportError() {
    const errorReport = {
      message: error?.message || 'Unknown error',
      stack: error?.stack || 'No stack trace',
      componentStack: componentStack,
      userAgent: navigator.userAgent,
      url: window.location.href,
      timestamp: new Date().toISOString(),
      additionalInfo: errorInfo
    };
    
    // Copy to clipboard
    if (browser && navigator.clipboard) {
      navigator.clipboard.writeText(JSON.stringify(errorReport, null, 2))
        .then(() => {
          toast.success('Error details copied to clipboard');
        })
        .catch(() => {
          toast.error('Failed to copy error details');
        });
    }
    
    console.log('Error Report:', errorReport);
  }
  
  // Helper function to check if error is recoverable
  function isRecoverable(err) {
    if (!err) return false;
    
    const recoverableErrors = [
      'Network Error',
      'Failed to fetch',
      'NetworkError',
      'TimeoutError',
      'AbortError'
    ];
    
    return recoverableErrors.some(pattern => 
      err.message?.includes(pattern) || err.name?.includes(pattern)
    );
  }
  
  // Determine error severity
  function getErrorSeverity(err) {
    if (!err) return 'low';
    
    const criticalPatterns = [
      'ChunkLoadError',
      'SecurityError',
      'ReferenceError',
      'TypeError'
    ];
    
    const highPatterns = [
      'SyntaxError',
      'RangeError',
      'URIError'
    ];
    
    if (criticalPatterns.some(pattern => err.name?.includes(pattern))) {
      return 'critical';
    }
    
    if (highPatterns.some(pattern => err.name?.includes(pattern))) {
      return 'high';
    }
    
    return 'medium';
  }
  
  let errorSeverity = $derived(getErrorSeverity(error));
  let recoverable = $derived(isRecoverable(error));
</script>

{#if hasError}
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    {#if fallback}
      <!-- Custom fallback component -->
      <svelte:component this={fallback} {error} {errorInfo} {retry} {reload} />
    {:else}
      <!-- Default error UI -->
      <Card class="max-w-lg w-full">
        <div class="text-center">
          <!-- Error Icon -->
          <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-red-100 mb-4">
            {#if errorSeverity === 'critical'}
              <svg class="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            {:else}
              <svg class="h-8 w-8 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            {/if}
          </div>
          
          <!-- Error Title -->
          <h2 class="text-xl font-semibold text-gray-900 mb-2">
            {#if errorSeverity === 'critical'}
              Critical Error Occurred
            {:else if errorSeverity === 'high'}
              System Error
            {:else}
              Something went wrong
            {/if}
          </h2>
          
          <!-- Error Message -->
          <p class="text-gray-600 mb-4">
            {#if customMessage}
              {customMessage}
            {:else if error?.message}
              {error.message}
            {:else}
              An unexpected error occurred. Please try again.
            {/if}
          </p>
          
          <!-- Error Details (if enabled) -->
          {#if showDetails && error}
            <details class="text-left mb-4 bg-gray-50 p-4 rounded-lg">
              <summary class="cursor-pointer font-medium text-gray-700 mb-2">
                Technical Details
              </summary>
              <div class="text-sm text-gray-600 space-y-2">
                <div>
                  <strong>Error Type:</strong> {error.name || 'Unknown'}
                </div>
                <div>
                  <strong>Severity:</strong> 
                  <span class="capitalize inline-flex items-center px-2 py-1 rounded-full text-xs font-medium {
                    errorSeverity === 'critical' ? 'bg-red-100 text-red-800' :
                    errorSeverity === 'high' ? 'bg-orange-100 text-orange-800' :
                    'bg-yellow-100 text-yellow-800'
                  }">
                    {errorSeverity}
                  </span>
                </div>
                {#if componentStack}
                  <div>
                    <strong>Component Stack:</strong>
                    <pre class="mt-1 text-xs bg-white p-2 rounded border overflow-x-auto">{componentStack}</pre>
                  </div>
                {/if}
                {#if errorInfo?.source}
                  <div>
                    <strong>Source:</strong> {errorInfo.source}:{errorInfo.line}
                  </div>
                {/if}
              </div>
            </details>
          {/if}
          
          <!-- Recovery Actions -->
          <div class="flex flex-col sm:flex-row gap-3 justify-center">
            {#if recoverable}
              <Button on:click={retry} variant="primary">
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Try Again
              </Button>
            {/if}
            
            {#if showReload}
              <Button on:click={reload} variant={recoverable ? 'outline' : 'primary'}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Reload Page
              </Button>
            {/if}
            
            <Button on:click={reportError} variant="ghost" size="sm">
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V9a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              Copy Details
            </Button>
          </div>
          
          <!-- Help Text -->
          <p class="text-sm text-gray-500 mt-4">
            If this problem persists, please contact support with the error details.
          </p>
        </div>
      </Card>
    {/if}
  </div>
{:else}
  <!-- Render children when no error -->
  {@render children?.()}
{/if}