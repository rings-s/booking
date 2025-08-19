<!-- src/lib/components/common/Button.svelte -->
<script>
    let {
        type = 'button',
        variant = 'primary',
        size = 'md',
        disabled = false,
        loading = false,
        fullWidth = false,
        href = null,
        onclick = () => {},
        children,
        ...restProps
    } = $props();
  
    const variants = {
      primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
      secondary: 'bg-white text-blue-600 hover:bg-blue-50 focus:ring-blue-500 border-2 border-blue-600',
      success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500',
      danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
      outline: 'border-2 border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-gray-500'
    };
  
    const sizes = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg'
    };
  
    let classes = $derived(`
      ${variants[variant]}
      ${sizes[size]}
      ${fullWidth ? 'w-full' : ''}
      ${disabled || loading ? 'opacity-50 cursor-not-allowed' : ''}
      inline-flex items-center justify-center
      font-medium rounded-md
      focus:outline-none focus:ring-2 focus:ring-offset-2
      transition-colors duration-200
    `);
  </script>
  
  {#if href && !disabled}
    <a {href} class={classes} {onclick}>
      {#if loading}
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      {/if}
      {@render children?.()}
    </a>
  {:else}
    <button
      {type}
      {disabled}
      class={classes}
      {onclick}
    >
      {#if loading}
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      {/if}
      {@render children?.()}
    </button>
  {/if}