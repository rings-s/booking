<!-- src/lib/components/common/Button.svelte -->
<script>
    export let type = 'button';
    export let variant = 'primary';
    export let size = 'md';
    export let disabled = false;
    export let loading = false;
    export let fullWidth = false;
    export let href = null;
  
    const variants = {
      primary: 'bg-indigo-600 text-white hover:bg-indigo-700 focus:ring-indigo-500',
      secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
      success: 'bg-green-600 text-white hover:bg-green-700 focus:ring-green-500',
      danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
      outline: 'border-2 border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-gray-500'
    };
  
    const sizes = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg'
    };
  
    $: classes = `
      ${variants[variant]}
      ${sizes[size]}
      ${fullWidth ? 'w-full' : ''}
      ${disabled || loading ? 'opacity-50 cursor-not-allowed' : ''}
      inline-flex items-center justify-center
      font-medium rounded-md
      focus:outline-none focus:ring-2 focus:ring-offset-2
      transition-colors duration-200
    `;
  </script>
  
  {#if href && !disabled}
    <a {href} class={classes} on:click>
      {#if loading}
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      {/if}
      <slot />
    </a>
  {:else}
    <button
      {type}
      {disabled}
      class={classes}
      on:click
    >
      {#if loading}
        <svg class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
      {/if}
      <slot />
    </button>
  {/if}