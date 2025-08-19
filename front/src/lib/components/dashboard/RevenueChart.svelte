<!-- src/lib/components/dashboard/RevenueChart.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';
    import { formatCurrency } from '$lib/utils/formatters';
    import Card from '../common/Card.svelte';
    import Select from '../common/Select.svelte';
    import Button from '../common/Button.svelte';
    import Spinner from '../common/Spinner.svelte';
    
    let {
        data = [],
        loading = false,
        title = 'Revenue Overview',
        height = '300px',
        period = 'month', // 'week', 'month', 'quarter', 'year'
        comparison = false,
        previousData = [],
        onperiodchange = () => {},
        ...restProps
    } = $props();
    
    let canvas = $state();
    let chart = $state();
    let selectedPeriod = $state(period);
    let chartType = $state('line'); // 'line', 'bar'
    
    const periodOptions = [
      { value: 'week', label: 'This Week' },
      { value: 'month', label: 'This Month' },
      { value: 'quarter', label: 'This Quarter' },
      { value: 'year', label: 'This Year' }
    ];
    
    onMount(() => {
      if (dataArray.length > 0) {
        initChart();
      }
      
      return () => {
        if (chart) {
          chart.destroy();
        }
      };
    });
    
    $effect(() => {
      console.log('RevenueChart $effect:', {
        hasCanvas: !!canvas,
        dataLength: dataArray.length,
        hasChart: !!chart,
        data: dataArray.slice(0, 3)
      });
      
      if (canvas && dataArray.length > 0) {
        if (chart) {
          console.log('RevenueChart: Updating existing chart');
          updateChart();
        } else {
          console.log('RevenueChart: Initializing new chart');
          initChart();
        }
      }
    });
    
    function initChart() {
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      
      const datasets = [{
        label: 'Current Period',
        data: dataArray.map(d => d.revenue || d.value || 0),
        borderColor: 'rgb(79, 70, 229)',
        backgroundColor: chartType === 'bar' ? 'rgba(79, 70, 229, 0.8)' : 'rgba(79, 70, 229, 0.1)',
        tension: 0.3,
        fill: chartType === 'line'
      }];
      
      if (comparison && previousData.length > 0) {
        datasets.push({
          label: 'Previous Period',
          data: previousData.map(d => d.revenue || d.value || 0),
          borderColor: 'rgb(156, 163, 175)',
          backgroundColor: chartType === 'bar' ? 'rgba(156, 163, 175, 0.5)' : 'rgba(156, 163, 175, 0.1)',
          tension: 0.3,
          fill: chartType === 'line',
          borderDash: [5, 5]
        });
      }
      
      chart = new Chart(ctx, {
        type: chartType,
        data: {
          labels: dataArray.map(d => d.label || d.month || d.date || ''),
          datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false
          },
          plugins: {
            legend: {
              display: comparison,
              position: 'top',
              labels: {
                usePointStyle: true,
                padding: 15
              }
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const label = context.dataset.label || '';
                  const value = formatCurrency(context.parsed.y);
                  return `${label}: ${value}`;
                },
                footer: (tooltipItems) => {
                  const sum = tooltipItems.reduce((a, b) => a + b.parsed.y, 0);
                  return `Total: ${formatCurrency(sum)}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: {
                display: false
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                callback: (value) => formatCurrency(value)
              },
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              }
            }
          }
        }
      });
    }
    
    function updateChart() {
      if (!chart) return;
      
      chart.data.labels = data.map(d => d.label || d.month || d.date || '');
      chart.data.datasets[0].data = data.map(d => d.revenue || d.value || 0);
      
      if (comparison && previousData.length > 0 && chart.data.datasets[1]) {
        chart.data.datasets[1].data = previousData.map(d => d.revenue || d.value || 0);
      }
      
      chart.update();
    }
    
    function toggleChartType() {
      chartType = chartType === 'line' ? 'bar' : 'line';
      if (chart) {
        chart.destroy();
        initChart();
      }
    }
    
    function handlePeriodChange() {
      // Dispatch event to parent to reload data
      onperiodchange(selectedPeriod);
    }
    
    // Calculate summary stats - ensure data is always an array
    let dataArray = $derived(Array.isArray(data) ? data : []);
    let totalRevenue = $derived(dataArray.reduce((sum, d) => sum + (d.revenue || d.value || 0), 0));
    let averageRevenue = $derived(dataArray.length > 0 ? totalRevenue / dataArray.length : 0);
    let maxRevenue = $derived(dataArray.length > 0 ? Math.max(...dataArray.map(d => d.revenue || d.value || 0)) : 0);
    let minRevenue = $derived(dataArray.length > 0 ? Math.min(...dataArray.map(d => d.revenue || d.value || 0)) : 0);
  </script>
  
  <Card >
    {#snippet header()}
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">{title}</h3>
        <div class="flex items-center space-x-2">
          <Select
            bind:value={selectedPeriod}
            options={periodOptions}
            on:change={handlePeriodChange}
          />
          <Button
            variant="outline"
            size="sm"
            on:click={toggleChartType}
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {#if chartType === 'line'}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              {:else}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
              {/if}
            </svg>
          </Button>
        </div>
      </div>
    {/snippet}
    
    {#if loading}
      <div class="flex items-center justify-center" style="height: {height}">
        <Spinner size="lg">Loading revenue data...</Spinner>
      </div>
    {:else if dataArray.length > 0}
      <!-- Summary Stats -->
      <div class="grid grid-cols-4 gap-4 mb-4">
        <div class="text-center">
          <p class="text-xs text-gray-500">Total</p>
          <p class="text-sm font-semibold text-gray-900">{formatCurrency(totalRevenue)}</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-500">Average</p>
          <p class="text-sm font-semibold text-gray-900">{formatCurrency(averageRevenue)}</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-500">Highest</p>
          <p class="text-sm font-semibold text-gray-900">{formatCurrency(maxRevenue)}</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-500">Lowest</p>
          <p class="text-sm font-semibold text-gray-900">{formatCurrency(minRevenue)}</p>
        </div>
      </div>
      
      <!-- Chart -->
      <div style="height: {height}">
        <canvas bind:this={canvas}></canvas>
      </div>
    {:else}
      <div class="flex items-center justify-center text-gray-500" style="height: {height}">
        <div class="text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p class="mt-2 text-sm">No revenue data available</p>
        </div>
      </div>
    {/if}
  </Card>