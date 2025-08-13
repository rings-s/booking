<!-- src/lib/components/dashboard/ServiceChart.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';
    import { formatCurrency } from '$lib/utils/formatters';
    import Card from '../common/Card.svelte';
    import Select from '../common/Select.svelte';
    import Spinner from '../common/Spinner.svelte';
    
    export let data = [];
    export let loading = false;
    export let title = 'Service Performance';
    export let height = '300px';
    export let chartType = 'doughnut'; // 'doughnut', 'bar', 'horizontal-bar'
    export let metric = 'bookings'; // 'bookings', 'revenue'
    
    let canvas;
    let chart;
    let selectedChartType = chartType;
    let selectedMetric = metric;
    
    const chartTypeOptions = [
      { value: 'doughnut', label: 'Doughnut' },
      { value: 'bar', label: 'Bar' },
      { value: 'horizontal-bar', label: 'Horizontal Bar' }
    ];
    
    const metricOptions = [
      { value: 'bookings', label: 'By Bookings' },
      { value: 'revenue', label: 'By Revenue' }
    ];
    
    const colors = [
      'rgba(79, 70, 229, 0.8)',
      'rgba(16, 185, 129, 0.8)',
      'rgba(245, 158, 11, 0.8)',
      'rgba(239, 68, 68, 0.8)',
      'rgba(139, 92, 246, 0.8)',
      'rgba(6, 182, 212, 0.8)',
      'rgba(236, 72, 153, 0.8)',
      'rgba(34, 197, 94, 0.8)'
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
    
    $: if (chart && dataArray.length > 0) {
      updateChart();
    }
    
    function initChart() {
      const ctx = canvas.getContext('2d');
      
      const chartData = processData(data);
      
      chart = new Chart(ctx, {
        type: selectedChartType === 'horizontal-bar' ? 'bar' : selectedChartType,
        data: {
          labels: chartData.labels,
          datasets: [{
            label: selectedMetric === 'bookings' ? 'Bookings' : 'Revenue',
            data: chartData.values,
            backgroundColor: colors,
            borderColor: colors.map(c => c.replace('0.8', '1')),
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: selectedChartType === 'horizontal-bar' ? 'y' : 'x',
          plugins: {
            legend: {
              display: selectedChartType === 'doughnut',
              position: 'right',
              labels: {
                padding: 10,
                font: {
                  size: 11
                }
              }
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const label = context.label || '';
                  const value = context.parsed || context.parsed.y || 0;
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(1);
                  
                  if (selectedMetric === 'revenue') {
                    return `${label}: ${formatCurrency(value)} (${percentage}%)`;
                  }
                  return `${label}: ${value} bookings (${percentage}%)`;
                }
              }
            }
          },
          scales: selectedChartType !== 'doughnut' ? {
            x: {
              grid: {
                display: false
              },
              ticks: {
                callback: (value) => {
                  if (selectedMetric === 'revenue' && selectedChartType !== 'horizontal-bar') {
                    return formatCurrency(value);
                  }
                  return value;
                }
              }
            },
            y: {
              beginAtZero: true,
              ticks: {
                callback: (value) => {
                  if (selectedMetric === 'revenue' && selectedChartType === 'horizontal-bar') {
                    return formatCurrency(value);
                  }
                  return value;
                }
              }
            }
          } : {}
        }
      });
    }
    
    function processData(rawData) {
      const sortedData = [...rawData].sort((a, b) => {
        const valueA = selectedMetric === 'revenue' ? (b.revenue || 0) : (b.bookings || b.count || 0);
        const valueB = selectedMetric === 'revenue' ? (a.revenue || 0) : (a.bookings || a.count || 0);
        return valueA - valueB;
      });
      
      // Limit to top 8 services
      const topData = sortedData.slice(0, 8);
      
      return {
        labels: topData.map(d => d.name || d.service_name || 'Unknown'),
        values: topData.map(d => selectedMetric === 'revenue' ? (d.revenue || 0) : (d.bookings || d.count || 0))
      };
    }
    
    function updateChart() {
      if (!chart) return;
      
      const chartData = processData(data);
      
      if (chart.config.type !== (selectedChartType === 'horizontal-bar' ? 'bar' : selectedChartType)) {
        chart.destroy();
        initChart();
      } else {
        chart.data.labels = chartData.labels;
        chart.data.datasets[0].data = chartData.values;
        chart.options.indexAxis = selectedChartType === 'horizontal-bar' ? 'y' : 'x';
        chart.update();
      }
    }
    
    function handleChartTypeChange() {
      if (chart) {
        chart.destroy();
        initChart();
      }
    }
    
    function handleMetricChange() {
      updateChart();
    }
    
    // Calculate top service - ensure data is always an array
    $: dataArray = Array.isArray(data) ? data : [];
    $: topService = dataArray.reduce((max, service) => {
      const value = selectedMetric === 'revenue' ? (service.revenue || 0) : (service.bookings || service.count || 0);
      const maxValue = selectedMetric === 'revenue' ? (max.revenue || 0) : (max.bookings || max.count || 0);
      return value > maxValue ? service : max;
    }, dataArray[0] || {});
  </script>
  
  <Card>
    <div slot="header" class="flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900">{title}</h3>
      <div class="flex items-center space-x-2">
        <Select
          bind:value={selectedMetric}
          options={metricOptions}
          on:change={handleMetricChange}
        />
        <Select
          bind:value={selectedChartType}
          options={chartTypeOptions}
          on:change={handleChartTypeChange}
        />
      </div>
    </div>
    
    {#if loading}
      <div class="flex items-center justify-center" style="height: {height}">
        <Spinner size="lg">Loading service data...</Spinner>
      </div>
    {:else if dataArray.length > 0}
      <!-- Top Service Highlight -->
      {#if topService}
        <div class="mb-4 p-3 bg-indigo-50 rounded-lg">
          <p class="text-xs text-indigo-600 font-medium">Top Service</p>
          <p class="text-sm font-semibold text-gray-900">{topService.name || topService.service_name}</p>
          <p class="text-xs text-gray-600">
            {selectedMetric === 'revenue' 
              ? formatCurrency(topService.revenue || 0)
              : `${topService.bookings || topService.count || 0} bookings`}
          </p>
        </div>
      {/if}
      
      <!-- Chart -->
      <div style="height: {height}">
        <canvas bind:this={canvas}></canvas>
      </div>
    {:else}
      <div class="flex items-center justify-center text-gray-500" style="height: {height}">
        <div class="text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <p class="mt-2 text-sm">No service data available</p>
        </div>
      </div>
    {/if}
  </Card>