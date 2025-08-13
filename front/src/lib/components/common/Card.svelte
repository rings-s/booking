<!-- src/lib/components/common/Card.svelte -->
<script>
    export let title = '';
    export let subtitle = '';
    export let shadow = 'md';
    export let padding = 'md';
    export let hoverable = false;
    
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
    on:click
    on:keydown
  >
    {#if title || subtitle || $$slots.header}
      <div class="mb-4">
        {#if $$slots.header}
          <slot name="header" />
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
      <slot />
    </div>
    
    {#if $$slots.footer}
      <div class="mt-4 pt-4 border-t border-gray-200">
        <slot name="footer" />
      </div>
    {/if}
  </div>