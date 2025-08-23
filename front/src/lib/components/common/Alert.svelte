<!-- src/lib/components/common/Alert.svelte -->
<script>
    let {
        type = 'info',
        title = '',
        message = '',
        dismissible = false,
        icon = true,
        children,
        ondismiss = () => {},
        ...restProps
    } = $props();
    
    const types = {
      success: {
        bg: 'bg-green-50',
        border: 'border-green-400',
        text: 'text-green-800',
        icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z'
      },
      error: {
        bg: 'bg-red-50',
        border: 'border-red-400',
        text: 'text-red-800',
        icon: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z'
      },
      warning: {
        bg: 'bg-yellow-50',
        border: 'border-yellow-400',
        text: 'text-yellow-800',
        icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'
      },
      info: {
        bg: 'bg-blue-50',
        border: 'border-blue-400',
        text: 'text-blue-800',
        icon: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
      }
    };
    
    let style = $derived(types[type]);
    
    function dismiss() {
      ondismiss();
    }
  </script>
  
  <div class="rounded-md {style.bg} border {style.border} p-4">
    <div class="flex">
      {#if icon}
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 {style.text}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={style.icon} />
          </svg>
        </div>
      {/if}
      
      <div class="ml-3 flex-1">
        {#if title}
          <h3 class="text-sm font-medium {style.text}">{title}</h3>
        {/if}
        {#if message}
          <div class="text-sm {style.text} {title ? 'mt-2' : ''}">
            {message}
          </div>
        {/if}
        {@render children?.()}
      </div>
      
      {#if dismissible}
        <div class="ml-auto pl-3">
          <button
            type="button"
            class="-m-1.5 inline-flex rounded-md p-1.5 {style.text} hover:bg-opacity-20 focus:outline-none"
            onclick={dismiss}
          >
            <span class="sr-only">Dismiss</span>
            <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      {/if}
    </div>
  </div>