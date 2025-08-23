<!-- src/lib/components/common/Card.svelte -->
<script>
    let {
        title = '',
        subtitle = '',
        shadow = 'md',
        padding = 'md',
        hoverable = false,
        children,
        header,
        footer,
        ...restProps
    } = $props();
    
    const shadows = {
      none: '',
      sm: 'shadow-sm',
      md: 'shadow-md',
      lg: 'shadow-lg',
      xl: 'shadow-xl'
    };
    
    const paddings = {
      none: '',
      sm: 'p-4',
      md: 'p-6',
      lg: 'p-8'
    };
  </script>
  
  <div
    class="
      bg-white rounded-lg
      {shadows[shadow]}
      {paddings[padding]}
      {hoverable ? 'hover:shadow-lg transition-shadow cursor-pointer' : ''}
    "
    {...restProps}
    role={hoverable ? 'button' : 'region'}
    tabindex={hoverable ? '0' : undefined}
  >
    {#if title || subtitle || header}
      <div class="mb-4">
        {#if header}
          {@render header()}
        {:else}
          {#if title}
            <h3 class="text-lg font-semibold text-gray-900">{title}</h3>
          {/if}
          {#if subtitle}
            <p class="text-sm text-gray-500 mt-1">{subtitle}</p>
          {/if}
        {/if}
      </div>
    {/if}
    
    <div>
      {@render children?.()}
    </div>
    
    {#if footer}
      <div class="mt-4 pt-4 border-t border-gray-200">
        {@render footer()}
      </div>
    {/if}
  </div>