<!-- src/lib/components/common/Avatar.svelte -->
<script>
    export let src = '';
    export let alt = '';
    export let name = '';
    export let size = 'md';
    export let rounded = 'full';
    
    const sizes = {
      xs: 'h-6 w-6 text-xs',
      sm: 'h-8 w-8 text-sm',
      md: 'h-10 w-10 text-base',
      lg: 'h-12 w-12 text-lg',
      xl: 'h-16 w-16 text-xl'
    };
    
    const roundeds = {
      none: '',
      sm: 'rounded',
      md: 'rounded-md',
      lg: 'rounded-lg',
      full: 'rounded-full'
    };
    
    function getInitials(name) {
      if (!name) return '?';
      const parts = name.split(' ');
      if (parts.length >= 2) {
        return parts[0][0] + parts[parts.length - 1][0];
      }
      return name.slice(0, 2).toUpperCase();
    }
  </script>
  
  <div class="{sizes[size]} {roundeds[rounded]} overflow-hidden bg-gray-200 relative">
    {#if src}
      <img
        {src}
        {alt}
        class="h-full w-full object-cover"
        on:error={() => src = ''}
      />
    {:else}
      <div class="h-full w-full bg-indigo-600 flex items-center justify-center text-white font-medium">
        {getInitials(name)}
      </div>
    {/if}
  </div>