<!-- src/routes/auth/google/callback/+page.svelte -->
<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { authAPI } from '$lib/api/auth';
  import { auth } from '$lib/stores/auth';
  import toast from 'svelte-french-toast';
  
  let loading = true;
  let error = null;
  
  onMount(async () => {
    try {
      // Get parameters from URL
      const code = $page.url.searchParams.get('code');
      const state = $page.url.searchParams.get('state');
      const errorParam = $page.url.searchParams.get('error');
      const errorDescription = $page.url.searchParams.get('error_description');
      
      // Handle OAuth errors first
      if (errorParam) {
        let errorMessage = 'Google OAuth error';
        
        switch (errorParam) {
          case 'access_denied':
            errorMessage = 'Access denied. You need to grant permission to continue.';
            break;
          case 'invalid_request':
            errorMessage = 'Invalid authentication request.';
            break;
          case 'temporarily_unavailable':
            errorMessage = 'Google authentication is temporarily unavailable. Please try again later.';
            break;
          default:
            errorMessage = errorDescription || `Google OAuth error: ${errorParam}`;
        }
        
        throw new Error(errorMessage);
      }
      
      if (!code) {
        throw new Error('No authorization code received from Google');
      }
      
      // Validate state parameter for CSRF protection (if available)
      if (state && window.opener) {
        // This should match the state stored in the parent window
        console.info('OAuth state received:', state);
      }
      
      // Show progress
      console.info('Processing Google OAuth callback...');
      
      // Exchange code for tokens via our backend with timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
      
      try {
        const { data, error: apiError } = await authAPI.googleCallback(code);
        clearTimeout(timeoutId);
        
        if (apiError) {
          // Handle specific API errors
          let errorMessage = 'Authentication failed';
          
          if (typeof apiError === 'object') {
            errorMessage = apiError.detail || apiError.message || 'Authentication server error';
          } else if (typeof apiError === 'string') {
            errorMessage = apiError;
          }
          
          throw new Error(errorMessage);
        }
        
        if (!data || !data.user) {
          throw new Error('Invalid response from authentication server');
        }
        
        // Set user in auth store
        auth.setUser(data.user);
        
        const successMessage = `Welcome ${data.user.first_name || 'back'}! Successfully signed in.`;
        
        // Handle popup vs direct navigation
        if (window.opener && !window.opener.closed) {
          // We're in a popup - communicate with parent
          window.opener.postMessage({
            type: 'GOOGLE_AUTH_SUCCESS',
            data: data,
            message: successMessage
          }, window.location.origin);
          
          // Small delay before closing to ensure message is received
          setTimeout(() => {
            window.close();
          }, 100);
          
        } else {
          // Direct navigation (not in popup)
          toast.success(successMessage);
          setTimeout(() => {
            goto('/dashboard');
          }, 1000);
        }
        
      } catch (networkError) {
        clearTimeout(timeoutId);
        throw networkError;
      }
      
    } catch (err) {
      console.error('Google OAuth callback error:', err);
      error = err.message || 'Authentication failed';
      
      // Handle popup vs direct navigation for errors
      if (window.opener && !window.opener.closed) {
        // We're in a popup - communicate error to parent
        window.opener.postMessage({
          type: 'GOOGLE_AUTH_ERROR',
          error: error,
          details: err.stack
        }, window.location.origin);
        
        // Small delay before closing
        setTimeout(() => {
          window.close();
        }, 1000);
        
      } else {
        // Direct navigation - show error and redirect
        toast.error(error);
        setTimeout(() => {
          goto('/auth/login');
        }, 3000);
      }
      
    } finally {
      loading = false;
    }
  });
</script>

<svelte:head>
  <title>Google Sign-In - BookingPro</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 flex items-center justify-center">
  <div class="max-w-md w-full bg-white rounded-lg shadow-md p-8 text-center">
    {#if loading}
      <!-- Loading State -->
      <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mx-auto mb-4"></div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">Completing Google Sign-In...</h2>
      <p class="text-gray-600 mb-4">Please wait while we securely verify your account.</p>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div class="bg-indigo-600 h-2 rounded-full animate-pulse" style="width: 70%"></div>
      </div>
      <p class="text-sm text-gray-500 mt-2">This may take a few seconds...</p>
      
    {:else if error}
      <!-- Error State -->
      <div class="text-red-600 mb-4">
        <svg class="w-16 h-16 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      </div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">Authentication Failed</h2>
      <p class="text-gray-600 mb-4">{error}</p>
      <div class="bg-red-50 border border-red-200 rounded-md p-3 mb-4">
        <p class="text-sm text-red-700">If this problem persists, try:</p>
        <ul class="text-sm text-red-700 mt-2 list-disc list-inside">
          <li>Clearing your browser cookies</li>
          <li>Disabling ad blockers temporarily</li>
          <li>Using a different browser</li>
        </ul>
      </div>
      {#if window.opener}
        <p class="text-sm text-gray-500">This window will close automatically...</p>
      {:else}
        <p class="text-sm text-gray-500">Redirecting to login page...</p>
      {/if}
      
    {:else}
      <!-- Success State -->
      <div class="text-green-600 mb-4">
        <svg class="w-16 h-16 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">Sign-In Successful!</h2>
      <p class="text-gray-600 mb-4">You have been successfully authenticated with Google.</p>
      {#if window.opener}
        <p class="text-sm text-gray-500">You can now close this window or it will close automatically.</p>
      {:else}
        <p class="text-sm text-gray-500">Redirecting to your dashboard...</p>
        <div class="mt-4">
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-green-600 h-2 rounded-full animate-pulse" style="width: 100%"></div>
          </div>
        </div>
      {/if}
    {/if}
  </div>
</div>