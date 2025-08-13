<!-- src/routes/businesses/[slug]/analytics/+page.svelte -->
<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { businessAPI } from '$lib/api/businesses';
    import { bookingAPI } from '$lib/api/bookings';
    import { reviewAPI } from '$lib/api/reviews';
    import StatsCard from '$lib/components/dashboard/StatsCard.svelte';
    import RevenueChart from '$lib/components/dashboard/RevenueChart.svelte';
    import BookingChart from '$lib/components/dashboard/BookingChart.svelte';
    import ServiceChart from '$lib/components/dashboard/ServiceChart.svelte';
    import CustomerChart from '$lib/components/dashboard/CustomerChart.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Select from '$lib/components/common/Select.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import toast from 'svelte-french-toast';
    
    const slug = $page.params.slug;
    
    let business = null;
    let loading = true;
    let selectedPeriod = 'month';
    let comparing = false;
    
    // Analytics data
    let stats = {};
    let revenueData = [];
    let bookingData = [];
    let serviceData = [];
    let customerData = {};
    let topCustomers = [];
    let peakHours = [];
    let conversionRate = 0;
    
    const periodOptions = [
      { value: 'week', label: 'Last 7 Days' },
      { value: 'month', label: 'Last 30 Days' },
      { value: 'quarter', label: 'Last 3 Months' },
      { value: 'year', label: 'Last Year' },
      { value: 'all', label: 'All Time' }
    ];
    
    onMount(async () => {
      await loadBusiness();
      await loadAnalytics();
    });
    
    async function loadBusiness() {
      const { data, error } = await businessAPI.getBySlug(slug);
      
      if (data) {
        business = data;
      } else {
        toast.error('Business not found');
        goto('/dashboard');
      }
    }
    
    async function loadAnalytics() {
      loading = true;
      
      const [
        statsRes,
        revenueRes,
        bookingsRes,
        servicesRes,
        customersRes,
        topCustomersRes,
        peakHoursRes
      ] = await Promise.all([
        businessAPI.getStats(business?.id, selectedPeriod),
        businessAPI.getRevenueData(business?.id, selectedPeriod),
        bookingAPI.getChartData(business?.id, selectedPeriod),
        businessAPI.getServiceStats(business?.id, selectedPeriod),
        businessAPI.getCustomerAnalytics(business?.id, selectedPeriod),
        businessAPI.getTopCustomers(business?.id, selectedPeriod),
        businessAPI.getPeakHours(business?.id)
      ]);
      
      if (statsRes.data) stats = statsRes.data;
      if (revenueRes.data) revenueData = revenueRes.data;
      if (bookingsRes.data) bookingData = bookingsRes.data;
      if (servicesRes.data) serviceData = servicesRes.data;
      if (customersRes.data) customerData = customersRes.data;
      if (topCustomersRes.data) topCustomers = topCustomersRes.data;
      if (peakHoursRes.data) peakHours = peakHoursRes.data;
      
      // Calculate conversion rate
      if (stats.total_views && stats.total_bookings) {
        conversionRate = ((stats.total_bookings / stats.total_views) * 100).toFixed(2);
      }
      
      loading = false;
    }
    
    async function exportReport() {
      const { data, error } = await businessAPI.exportAnalytics(business.id, selectedPeriod);
      
      if (data) {
        // Download the file
        const blob = new Blob([data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `analytics-${business.slug}-${selectedPeriod}.csv`;
        link.click();
        
        toast.success('Report exported successfully');
      }
    }
    
    function handlePeriodChange() {
      loadAnalytics();
    }
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Business Analytics</h1>
            <p class="mt-1 text-sm text-gray-600">
              {business?.name || 'Loading...'}
            </p>
          </div>
          
          <div class="flex items-center space-x-4">
            <Select
              bind:value={selectedPeriod}
              options={periodOptions}
              on:change={handlePeriodChange}
            />
            
            <Button variant="outline" on:click={exportReport}>
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Export
            </Button>
            
            <Button variant="outline" href="/businesses/{slug}">
              View Business
            </Button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {#if loading}
        <div class="flex justify-center py-12">
          <Spinner size="lg">Loading analytics...</Spinner>
        </div>
      {:else}
        <!-- Key Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Total Revenue"
            value={stats.total_revenue || 0}
            change={stats.revenue_change}
            changeType={stats.revenue_change >= 0 ? 'increase' : 'decrease'}
            format="currency"
            icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            color="green"
          />
          
          <StatsCard
            title="Total Bookings"
            value={stats.total_bookings || 0}
            change={stats.bookings_change}
            changeType={stats.bookings_change >= 0 ? 'increase' : 'decrease'}
            icon="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
            color="blue"
          />
          
          <StatsCard
            title="Conversion Rate"
            value={conversionRate}
            format="percentage"
            icon="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
            color="purple"
          />
          
          <StatsCard
            title="Avg Booking Value"
            value={stats.avg_booking_value || 0}
            change={stats.avg_value_change}
            changeType={stats.avg_value_change >= 0 ? 'increase' : 'decrease'}
            format="currency"
            icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            color="indigo"
          />
        </div>
        
        <!-- Charts -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <RevenueChart
            data={revenueData}
            period={selectedPeriod}
            comparison={comparing}
          />
          
          <BookingChart
            data={bookingData}
            groupBy="day"
          />
          
          <ServiceChart
            data={serviceData}
            chartType="bar"
          />
          
          <CustomerChart
            data={customerData}
            view="acquisition"
          />
        </div>
        
        <!-- Additional Insights -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Top Customers -->
          <Card title="Top Customers">
            <div class="space-y-3">
              {#each topCustomers.slice(0, 5) as customer, i}
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <span class="text-sm font-medium text-gray-500">#{i + 1}</span>
                    <div>
                      <p class="text-sm font-medium text-gray-900">{customer.name}</p>
                      <p class="text-xs text-gray-500">{customer.bookings} bookings</p>
                    </div>
                  </div>
                  <span class="text-sm font-semibold text-gray-900">
                    ${customer.total_spent}
                  </span>
                </div>
              {/each}
            </div>
          </Card>
          
          <!-- Peak Hours -->
          <Card title="Peak Booking Hours">
            <div class="space-y-2">
              {#each peakHours as hour}
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">{hour.time}</span>
                  <div class="flex items-center space-x-2">
                    <div class="w-32 bg-gray-200 rounded-full h-2">
                      <div
                        class="bg-indigo-600 h-2 rounded-full"
                        style="width: {hour.percentage}%"
                      ></div>
                    </div>
                    <span class="text-sm font-medium text-gray-900 w-12 text-right">
                      {hour.count}
                    </span>
                  </div>
                </div>
              {/each}
            </div>
          </Card>
          
          <!-- Quick Stats -->
          <Card title="Performance Metrics">
            <dl class="space-y-3">
              <div class="flex justify-between">
                <dt class="text-sm text-gray-600">Repeat Customer Rate</dt>
                <dd class="text-sm font-semibold text-gray-900">
                  {stats.repeat_rate || 0}%
                </dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-sm text-gray-600">Avg Response Time</dt>
                <dd class="text-sm font-semibold text-gray-900">
                  {stats.avg_response_time || 'N/A'}
                </dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-sm text-gray-600">Cancellation Rate</dt>
                <dd class="text-sm font-semibold text-gray-900">
                  {stats.cancellation_rate || 0}%
                </dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-sm text-gray-600">No-show Rate</dt>
                <dd class="text-sm font-semibold text-gray-900">
                  {stats.noshow_rate || 0}%
                </dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-sm text-gray-600">Avg Rating</dt>
                <dd class="text-sm font-semibold text-gray-900">
                  {stats.avg_rating || 0}/5.0
                </dd>
              </div>
            </dl>
          </Card>
        </div>
      {/if}
    </div>
  </div>