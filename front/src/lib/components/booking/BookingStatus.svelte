<!-- src/lib/components/booking/BookingStatus.svelte -->
<script>
    export let status;
    export let size = 'sm';
    export let showIcon = true;
    export let showLabel = true;
    
    const statusConfig = {
      pending: {
        color: 'yellow',
        bgColor: 'bg-yellow-50',
        borderColor: 'border-yellow-200',
        textColor: 'text-yellow-800',
        dotColor: 'bg-yellow-400',
        label: 'Pending',
        icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
        description: 'Awaiting confirmation'
      },
      confirmed: {
        color: 'blue',
        bgColor: 'bg-blue-50',
        borderColor: 'border-blue-200',
        textColor: 'text-blue-800',
        dotColor: 'bg-blue-400',
        label: 'Confirmed',
        icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
        description: 'Booking confirmed'
      },
      cancelled: {
        color: 'red',
        bgColor: 'bg-red-50',
        borderColor: 'border-red-200',
        textColor: 'text-red-800',
        dotColor: 'bg-red-400',
        label: 'Cancelled',
        icon: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
        description: 'Booking cancelled'
      },
      completed: {
        color: 'green',
        bgColor: 'bg-green-50',
        borderColor: 'border-green-200',
        textColor: 'text-green-800',
        dotColor: 'bg-green-400',
        label: 'Completed',
        icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
        description: 'Service completed'
      },
      no_show: {
        color: 'gray',
        bgColor: 'bg-gray-50',
        borderColor: 'border-gray-200',
        textColor: 'text-gray-800',
        dotColor: 'bg-gray-400',
        label: 'No Show',
        icon: 'M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
        description: 'Customer did not show up'
      },
      in_progress: {
        color: 'purple',
        bgColor: 'bg-purple-50',
        borderColor: 'border-purple-200',
        textColor: 'text-purple-800',
        dotColor: 'bg-purple-400',
        label: 'In Progress',
        icon: 'M13 10V3L4 14h7v7l9-11h-7z',
        description: 'Service in progress'
      }
    };
    
    $: config = statusConfig[status] || statusConfig.pending;
    
    const sizes = {
      xs: {
        wrapper: 'text-xs px-2 py-0.5',
        icon: 'w-3 h-3',
        dot: 'w-1.5 h-1.5'
      },
      sm: {
        wrapper: 'text-sm px-2.5 py-0.5',
        icon: 'w-4 h-4',
        dot: 'w-2 h-2'
      },
      md: {
        wrapper: 'text-sm px-3 py-1',
        icon: 'w-5 h-5',
        dot: 'w-2.5 h-2.5'
      },
      lg: {
        wrapper: 'text-base px-4 py-2',
        icon: 'w-6 h-6',
        dot: 'w-3 h-3'
      }
    };
    
    $: sizeConfig = sizes[size] || sizes.sm;
  </script>
  
  <span
    class="
      inline-flex items-center rounded-full font-medium
      {sizeConfig.wrapper}
      {config.bgColor}
      {config.textColor}
      border {config.borderColor}
    "
    title={config.description}
  >
    {#if showIcon}
      <svg class="{sizeConfig.icon} {showLabel ? 'mr-1.5' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={config.icon} />
      </svg>
    {:else}
      <span class="{sizeConfig.dot} {config.dotColor} rounded-full {showLabel ? 'mr-1.5' : ''}"></span>
    {/if}
    
    {#if showLabel}
      {config.label}
    {/if}
  </span>