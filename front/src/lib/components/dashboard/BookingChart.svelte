<!-- src/lib/components/dashboard/BookingChart.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';
    import { formatCurrency, formatNumber, formatDecimal } from '$lib/utils/formatters';
    import Card from '../common/Card.svelte';
    import Select from '../common/Select.svelte';
    import Spinner from '../common/Spinner.svelte';
    
    let {
        data = [],
        loading = false,
        title = 'Booking Trends',
        height = '300px',
        groupBy = 'day', // 'hour', 'day', 'week', 'month'
        ongroupbychange = () => {},
        onmetricchange = () => {},
        ...restProps
    } = $props();
    
    let canvas = $state();
    let chart = $state();
    let selectedGroupBy = $state(groupBy);
    let selectedMetric = $state('count'); // 'count', 'revenue'
    
    const groupByOptions = [
      { value: 'hour', label: 'By Hour' },
      { value: 'day', label: 'By Day' },
      { value: 'week', label: 'By Week' },
      { value: 'month', label: 'By Month' }
    ];
    
    const metricOptions = [
      { value: 'count', label: 'Number of Bookings' },
      { value: 'revenue', label: 'Revenue' }
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
      console.log('BookingChart $effect:', {
        hasCanvas: !!canvas,
        dataLength: dataArray.length,
        hasChart: !!chart,
        sampleData: dataArray.slice(0, 2),
        totalBookings: dataArray.reduce((sum, d) => sum + (d.bookings || 0), 0),
        totalRevenue: dataArray.reduce((sum, d) => sum + (d.revenue || 0), 0)
      });
      
      if (canvas && dataArray.length > 0) {
        if (chart) {
          console.log('BookingChart: Updating existing chart');
          updateChart();
        } else {
          console.log('BookingChart: Initializing new chart');
          initChart();
        }
      }
    });
    
    function initChart() {
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      
      // Process data based on groupBy
      const processedData = processData(dataArray);
      
      chart = new Chart(ctx, {
        type: selectedGroupBy === 'hour' ? 'bar' : 'line',
        data: {
          labels: processedData.labels,
          datasets: [{
            label: selectedMetric === 'count' ? 'Bookings' : 'Revenue',
            data: processedData.values,
            borderColor: 'rgb(79, 70, 229)',
            backgroundColor: selectedGroupBy === 'hour' ? 'rgba(79, 70, 229, 0.8)' : 'rgba(79, 70, 229, 0.1)',
            tension: 0.3,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  if (selectedMetric === 'revenue') {
                    return `Revenue: ${formatCurrency(context.parsed.y)}`;
                  }
                  return `Bookings: ${formatNumber(context.parsed.y)}`;
                },
                footer: (tooltipItems) => {
                  if (selectedMetric === 'revenue' && tooltipItems.length > 0) {
                    const total = tooltipItems.reduce((sum, item) => sum + item.parsed.y, 0);
                    return `Total: ${formatCurrency(total)}`;
                  }
                  return '';
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
                callback: (value) => {
                  if (selectedMetric === 'revenue') {
                    return formatCurrency(value);
                  }
                  return formatNumber(value);
                }
              },
              grid: {
                color: 'rgba(0, 0, 0, 0.05)'
              }
            }
          }
        }
      });
    }
    
    function processData(rawData) {
      const labels = [];
      const values = [];
      
      if (selectedGroupBy === 'hour') {
        // Group by hour of day
        const hourlyData = Array(24).fill(0);
        const hourlyRevenue = Array(24).fill(0);
        
        rawData.forEach(booking => {
          const hour = new Date(booking.start_time).getHours();
          hourlyData[hour]++;
          if (selectedMetric === 'revenue') {
            hourlyRevenue[hour] += booking.total_price || 0;
          }
        });
        
        for (let i = 0; i < 24; i++) {
          labels.push(`${i}:00`);
          values.push(selectedMetric === 'revenue' ? hourlyRevenue[i] : hourlyData[i]);
        }
      } else {
        // Process for day/week/month grouping
        rawData.forEach(item => {
          labels.push(item.label || item.date);
          values.push(selectedMetric === 'revenue' ? (item.revenue || 0) : (item.bookings || item.count || 0));
        });
      }
      
      return { labels, values };
    }
    
    function updateChart() {
      if (!chart) return;
      
      const processedData = processData(dataArray);
      chart.data.labels = processedData.labels;
      chart.data.datasets[0].data = processedData.values;
      chart.data.datasets[0].label = selectedMetric === 'count' ? 'Bookings' : 'Revenue';
      
      if (selectedGroupBy === 'hour') {
        chart.config.type = 'bar';
      } else {
        chart.config.type = 'line';
      }
      
      chart.update();
    }
    
    function handleGroupByChange() {
      try {
        if (chart) {
          chart.destroy();
          initChart();
        }
        ongroupbychange(selectedGroupBy);
      } catch (error) {
        console.error('Error changing group by:', error);
      }
    }
    
    function handleMetricChange() {
      try {
        updateChart();
        onmetricchange(selectedMetric);
      } catch (error) {
        console.error('Error changing metric:', error);
      }
    }
    
    // Calculate stats - ensure data is always an array
    let dataArray = $derived(Array.isArray(data) ? data : []);
    let totalBookings = $derived(dataArray.reduce((sum, d) => sum + (d.bookings || d.count || 1), 0));
    let totalRevenue = $derived(dataArray.reduce((sum, d) => sum + (d.revenue || d.total_price || 0), 0));
    let averageBookingsPerPeriod = $derived(dataArray.length > 0 ? totalBookings / dataArray.length : 0);
  </script>
  
  <Card >
    {#snippet header()}
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">{title}</h3>
        <div class="flex items-center space-x-2">
          <Select
            bind:value={selectedMetric}
            options={metricOptions}
            on:change={handleMetricChange}
          />
          <Select
            bind:value={selectedGroupBy}
            options={groupByOptions}
            on:change={handleGroupByChange}
          />
        </div>
      </div>
    {/snippet}
    
    {#if loading}
      <div class="flex items-center justify-center" style="height: {height}">
        <Spinner size="lg">Loading booking data...</Spinner>
      </div>
    {:else if dataArray.length > 0}
      <!-- Stats Summary -->
      <div class="grid grid-cols-3 gap-4 mb-4 p-3 bg-gray-50 rounded-lg">
        <div class="text-center">
          <p class="text-xs text-gray-500">Total Bookings</p>
          <p class="text-lg font-semibold text-gray-900">{totalBookings}</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-500">Total Revenue</p>
          <p class="text-lg font-semibold text-gray-900">{formatCurrency(totalRevenue)}</p>
        </div>
        <div class="text-center">
          <p class="text-xs text-gray-500">Avg per {selectedGroupBy}</p>
          <p class="text-lg font-semibold text-gray-900">{formatDecimal(averageBookingsPerPeriod)}</p>
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
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <p class="mt-2 text-sm">No booking data available</p>
        </div>
      </div>
    {/if}
  </Card>