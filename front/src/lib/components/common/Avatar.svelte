<!-- src/lib/components/common/Avatar.svelte -->
<script>
    let {
        src = '',
        alt = '',
        name = '',
        size = 'md',
        rounded = 'full',
        ...restProps
    } = $props();
    
    let imageError = $state(false);
    let imageSrc = $derived(imageError ? '' : src);
    
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
    {#if imageSrc}
      <img
        src={imageSrc}
        {alt}
        class="h-full w-full object-cover"
        onerror={() => imageError = true}
      />
    {:else}
      <div class="h-full w-full bg-indigo-600 flex items-center justify-center text-white font-medium">
        {getInitials(name)}
      </div>
    {/if}
  </div>