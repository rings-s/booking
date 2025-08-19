<!-- src/lib/components/common/Spinner.svelte -->
<script>
    let {
        size = 'md',
        color = 'indigo',
        fullScreen = false,
        children,
        ...restProps
    } = $props();
    
    const sizes = {
      sm: 'h-4 w-4',
      md: 'h-8 w-8',
      lg: 'h-12 w-12',
      xl: 'h-16 w-16'
    };
    
    const colors = {
      indigo: 'text-indigo-600',
      gray: 'text-gray-600',
      white: 'text-white',
      green: 'text-green-600',
      red: 'text-red-600'
    };
  </script>
  
  {#if fullScreen}
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6">
        <svg class="animate-spin {sizes[size]} {colors[color]} mx-auto" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        {#if children}
          <div class="mt-4 text-center text-gray-600">
            {@render children()}
          </div>
        {/if}
      </div>
    </div>
  {:else}
    <div class="flex justify-center items-center">
      <svg class="animate-spin {sizes[size]} {colors[color]}" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
  {/if}