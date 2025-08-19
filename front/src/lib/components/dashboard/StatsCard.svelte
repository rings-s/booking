<!-- src/lib/components/dashboard/StatsCard.svelte -->
<script>
    import { formatCurrency, formatPercentage } from '$lib/utils/formatters';
    
    let {
        title = '',
        value = 0,
        change = null,
        changeType = 'increase', // 'increase' or 'decrease'
        icon = null,
        loading = false,
        format = 'number', // 'number', 'currency', 'percentage'
        color = 'indigo', // 'indigo', 'green', 'yellow', 'red', 'blue', 'purple'
        description = '',
        trend = [],
        onClick = null,
        onclick = () => {},
        ...restProps
    } = $props();
    
    const colors = {
      indigo: 'bg-indigo-100 text-indigo-600',
      green: 'bg-green-100 text-green-600',
      yellow: 'bg-yellow-100 text-yellow-600',
      red: 'bg-red-100 text-red-600',
      blue: 'bg-blue-100 text-blue-600',
      purple: 'bg-purple-100 text-purple-600',
      gray: 'bg-gray-100 text-gray-600'
    };
    
    const bgColors = {
      indigo: 'bg-indigo-50',
      green: 'bg-green-50',
      yellow: 'bg-yellow-50',
      red: 'bg-red-50',
      blue: 'bg-blue-50',
      purple: 'bg-purple-50',
      gray: 'bg-gray-50'
    };
    
    function formatValue(val) {
      if (val === null || val === undefined) return '—';
      
      switch (format) {
        case 'currency':
          return formatCurrency(val);
        case 'percentage':
          return formatPercentage(val / 100);
        case 'decimal':
          return val.toFixed(2);
        default:
          return typeof val === 'number' ? val.toLocaleString() : val;
      }
    }
    
    function handleClick() {
      if (onClick) {
        onClick();
      }
      onclick();
    }
    
    // Calculate sparkline points for mini trend chart
    let sparklinePoints = $derived(trend.length > 0 ? calculateSparkline(trend) : '');
    
    function calculateSparkline(data) {
      if (data.length < 2) return '';
      
      const max = Math.max(...data);
      const min = Math.min(...data);
      const range = max - min || 1;
      const width = 100;
      const height = 30;
      
      return data.map((val, i) => {
        const x = (i / (data.length - 1)) * width;
        const y = height - ((val - min) / range) * height;
        return `${x},${y}`;
      }).join(' ');
    }
  </script>
  
  <div 
    class="bg-white rounded-lg shadow hover:shadow-lg transition-all duration-200 p-6 {onClick ? 'cursor-pointer' : ''}"
    on:click={handleClick}
    on:keydown={(e) => e.key === 'Enter' && handleClick()}
    role={onClick ? 'button' : 'article'}
    tabindex={onClick ? 0 : -1}
  >
    <div class="flex items-start justify-between">
      <div class="flex-1">
        <div class="flex items-center">
          {#if icon}
            <div class="flex-shrink-0">
              <div class="p-3 rounded-lg {colors[color]}">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={icon} />
                </svg>
              </div>
            </div>
          {/if}
          
          <div class="{icon ? 'ml-5' : ''} flex-1">
            <dt class="text-sm font-medium text-gray-500 truncate">
              {title}
            </dt>
            
            <dd class="mt-1 flex items-baseline">
              {#if loading}
                <div class="flex items-center space-x-2">
                  <div class="animate-pulse h-8 bg-gray-200 rounded w-24"></div>
                  <div class="animate-pulse h-4 bg-gray-200 rounded w-16"></div>
                </div>
              {:else}
                <div class="text-2xl font-semibold text-gray-900">
                  {formatValue(value)}
                </div>
                
                {#if change !== null}
                  <div class="ml-2 flex items-baseline text-sm font-semibold">
                    {#if changeType === 'increase'}
                      <svg class="self-center flex-shrink-0 h-4 w-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                      </svg>
                      <span class="text-green-600">{change}%</span>
                    {:else if changeType === 'decrease'}
                      <svg class="self-center flex-shrink-0 h-4 w-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                      <span class="text-red-600">{Math.abs(change)}%</span>
                    {:else}
                      <span class="text-gray-500">→ {change}%</span>
                    {/if}
                  </div>
                {/if}
              {/if}
            </dd>
            
            {#if description && !loading}
              <dd class="mt-1 text-xs text-gray-500">{description}</dd>
            {/if}
          </div>
        </div>
        
        {#if trend.length > 0 && !loading}
          <div class="mt-4">
            <svg class="w-full h-8" viewBox="0 0 100 30" preserveAspectRatio="none">
              <polyline
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                points={sparklinePoints}
                class="text-indigo-400"
              />
              <polyline
                fill="url(#gradient)"
                stroke="none"
                points={`0,30 ${sparklinePoints} 100,30`}
                opacity="0.1"
              />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" style="stop-color:rgb(79, 70, 229);stop-opacity:0.2" />
                  <stop offset="100%" style="stop-color:rgb(79, 70, 229);stop-opacity:0" />
                </linearGradient>
              </defs>
            </svg>
          </div>
        {/if}
      </div>
      
      {#if onClick}
        <div class="ml-4">
          <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </div>
      {/if}
    </div>
  </div>