<!-- src/lib/components/dashboard/CustomerChart.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';
    import Card from '../common/Card.svelte';
    import Select from '../common/Select.svelte';
    import Spinner from '../common/Spinner.svelte';
    import { formatPercentage } from '$lib/utils/formatters';
    
    export let data = [];
    export let loading = false;
    export let title = 'Customer Analytics';
    export let height = '300px';
    export let view = 'acquisition'; // 'acquisition', 'retention', 'demographics', 'satisfaction'
    
    let canvas;
    let chart;
    let selectedView = view;
    
    const viewOptions = [
      { value: 'acquisition', label: 'Customer Acquisition' },
      { value: 'retention', label: 'Retention Rate' },
      { value: 'demographics', label: 'Demographics' },
      { value: 'satisfaction', label: 'Satisfaction' }
    ];
    
    onMount(() => {
      if (data.length > 0 || (typeof data === 'object' && Object.keys(data).length > 0)) {
        initChart();
      }
      
      return () => {
        if (chart) {
          chart.destroy();
        }
      };
    });
    
    $: if (chart && (data.length > 0 || (typeof data === 'object' && Object.keys(data).length > 0))) {
      updateChart();
    }
    
    function initChart() {
      const ctx = canvas.getContext('2d');
      const chartConfig = getChartConfig();
      chart = new Chart(ctx, chartConfig);
    }
    
    function getChartConfig() {
      switch (selectedView) {
        case 'acquisition':
          return getAcquisitionConfig();
        case 'retention':
          return getRetentionConfig();
        case 'demographics':
          return getDemographicsConfig();
        case 'satisfaction':
          return getSatisfactionConfig();
        default:
          return getAcquisitionConfig();
      }
    }
    
    function getAcquisitionConfig() {
      const processedData = Array.isArray(data) ? data : data.acquisition || [];
      
      return {
        type: 'line',
        data: {
          labels: processedData.map(d => d.date || d.label),
          datasets: [
            {
              label: 'New Customers',
              data: processedData.map(d => d.new_customers || 0),
              borderColor: 'rgb(34, 197, 94)',
              backgroundColor: 'rgba(34, 197, 94, 0.1)',
              tension: 0.3,
              fill: true
            },
            {
              label: 'Returning Customers',
              data: processedData.map(d => d.returning_customers || 0),
              borderColor: 'rgb(79, 70, 229)',
              backgroundColor: 'rgba(79, 70, 229, 0.1)',
              tension: 0.3,
              fill: true
            }
          ]
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
              display: true,
              position: 'top'
            },
            tooltip: {
              callbacks: {
                footer: (tooltipItems) => {
                  const total = tooltipItems.reduce((a, b) => a + b.parsed.y, 0);
                  return `Total: ${total} customers`;
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
              beginAtZero: true
            }
          }
        }
      };
    }
    
    function getRetentionConfig() {
      const retentionData = data.retention || [];
      
      return {
        type: 'bar',
        data: {
          labels: retentionData.map(d => d.cohort || d.label),
          datasets: [{
            label: 'Retention Rate',
            data: retentionData.map(d => d.rate || 0),
            backgroundColor: 'rgba(79, 70, 229, 0.8)',
            borderColor: 'rgb(79, 70, 229)',
            borderWidth: 1
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
                  return `Retention Rate: ${context.parsed.y.toFixed(1)}%`;
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
              max: 100,
              ticks: {
                callback: (value) => `${value}%`
              }
            }
          }
        }
      };
    }
    
    function getDemographicsConfig() {
      const demographics = data.demographics || {};
      
      return {
        type: 'doughnut',
        data: {
          labels: Object.keys(demographics),
          datasets: [{
            data: Object.values(demographics),
            backgroundColor: [
              'rgba(79, 70, 229, 0.8)',
              'rgba(34, 197, 94, 0.8)',
              'rgba(245, 158, 11, 0.8)',
              'rgba(239, 68, 68, 0.8)',
              'rgba(139, 92, 246, 0.8)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: 'right'
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((context.parsed / total) * 100).toFixed(1);
                  return `${context.label}: ${context.parsed} (${percentage}%)`;
                }
              }
            }
          }
        }
      };
    }
    
    function getSatisfactionConfig() {
      const satisfactionData = data.satisfaction || [];
      
      return {
        type: 'radar',
        data: {
          labels: satisfactionData.map(d => d.aspect || d.label),
          datasets: [{
            label: 'Customer Satisfaction',
            data: satisfactionData.map(d => d.score || 0),
            borderColor: 'rgb(79, 70, 229)',
            backgroundColor: 'rgba(79, 70, 229, 0.2)',
            pointBackgroundColor: 'rgb(79, 70, 229)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(79, 70, 229)'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            r: {
              beginAtZero: true,
              max: 5,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      };
    }
    
    function updateChart() {
      if (!chart) return;
      
      chart.destroy();
      initChart();
    }
    
    function handleViewChange() {
      if (chart) {
        chart.destroy();
        initChart();
      }
    }
    
    // Calculate key metrics - ensure data is always safe to use
    $: dataArray = Array.isArray(data) ? data : [];
    $: retentionArray = Array.isArray(data?.retention) ? data.retention : [];
    
    $: totalCustomers = dataArray.length > 0
      ? dataArray.reduce((sum, d) => sum + (d.new_customers || 0) + (d.returning_customers || 0), 0)
      : data?.total || 0;
    
    $: averageRetention = retentionArray.length > 0
      ? retentionArray.reduce((sum, d) => sum + (d.rate || 0), 0) / retentionArray.length
      : 0;
  </script>
  
  <Card>
    <div slot="header" class="flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900">{title}</h3>
      <Select
        bind:value={selectedView}
        options={viewOptions}
        on:change={handleViewChange}
      />
    </div>
    
    {#if loading}
      <div class="flex items-center justify-center" style="height: {height}">
        <Spinner size="lg">Loading customer data...</Spinner>
      </div>
    {:else if data && (Array.isArray(data) ? data.length > 0 : Object.keys(data).length > 0)}
      <!-- Key Metrics -->
      <div class="grid grid-cols-3 gap-4 mb-4">
        {#if selectedView === 'acquisition'}
          <div class="text-center p-2 bg-gray-50 rounded">
            <p class="text-xs text-gray-500">Total Customers</p>
            <p class="text-lg font-semibold text-gray-900">{totalCustomers}</p>
          </div>
          <div class="text-center p-2 bg-gray-50 rounded">
            <p class="text-xs text-gray-500">New This Month</p>
            <p class="text-lg font-semibold text-green-600">
              {data[data.length - 1]?.new_customers || 0}
            </p>
          </div>
          <div class="text-center p-2 bg-gray-50 rounded">
            <p class="text-xs text-gray-500">Returning</p>
            <p class="text-lg font-semibold text-indigo-600">
              {data[data.length - 1]?.returning_customers || 0}
            </p>
          </div>
        {:else if selectedView === 'retention'}
          <div class="col-span-3 text-center p-2 bg-gray-50 rounded">
            <p class="text-xs text-gray-500">Average Retention Rate</p>
            <p class="text-2xl font-semibold text-gray-900">{averageRetention.toFixed(1)}%</p>
          </div>
        {/if}
      </div>
      
      <!-- Chart -->
      <div style="height: {height}">
        <canvas bind:this={canvas}></canvas>
      </div>
    {:else}
      <div class="flex items-center justify-center text-gray-500" style="height: {height}">
        <div class="text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <p class="mt-2 text-sm">No customer data available</p>
        </div>
      </div>
    {/if}
  </Card>