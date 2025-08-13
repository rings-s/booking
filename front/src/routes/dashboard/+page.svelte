<!-- src/routes/dashboard/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { auth } from '$lib/stores/auth';
    import { businessAPI } from '$lib/api/businesses';
    import { bookingAPI } from '$lib/api/bookings';
    import { customerAPI } from '$lib/api/customers';
    import StatsCard from '$lib/components/dashboard/StatsCard.svelte';
    import RevenueChart from '$lib/components/dashboard/RevenueChart.svelte';
    import BookingChart from '$lib/components/dashboard/BookingChart.svelte';
    import ServiceChart from '$lib/components/dashboard/ServiceChart.svelte';
    import CustomerChart from '$lib/components/dashboard/CustomerChart.svelte';
    import RecentActivity from '$lib/components/dashboard/RecentActivity.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Select from '$lib/components/common/Select.svelte';
    import toast from 'svelte-french-toast';
    
    let loading = true;
    let selectedPeriod = 'month';
    let selectedBusiness = null;
    let businesses = [];
    
    // Dashboard data
    let stats = {
      revenue: 0,
      bookings: 0,
      customers: 0,
      rating: 0,
      revenueChange: 0,
      bookingsChange: 0,
      customersChange: 0,
      ratingChange: 0
    };
    
    let revenueData = [];
    let bookingData = [];
    let serviceData = [];
    let customerData = {};
    let activities = [];
    
    const periodOptions = [
      { value: 'week', label: 'This Week' },
      { value: 'month', label: 'This Month' },
      { value: 'quarter', label: 'This Quarter' },
      { value: 'year', label: 'This Year' }
    ];
    
    onMount(async () => {
      await loadBusinesses();
      await loadDashboardData();
    });
    
    async function loadBusinesses() {
      const { data, error } = await businessAPI.getMyBusinesses();
      if (data && Array.isArray(data) && data.length > 0) {
        businesses = data;
        selectedBusiness = businessAPI.getBusinessIdentifier(data[0]); // Use slug for API calls
      } else {
        businesses = [];
        selectedBusiness = null;
        if (error) {
          console.error('Failed to load businesses:', error);
          toast.error('Failed to load businesses. Please check your login status.');
        }
      }
    }
    
    async function loadDashboardData() {
      if (!selectedBusiness) {
        loading = false;
        return;
      }
      
      loading = true;
      
      // Load all dashboard data in parallel
      const [statsRes, revenueRes, bookingsRes, servicesRes, customersRes, activitiesRes] = await Promise.all([
        businessAPI.getStats(selectedBusiness, selectedPeriod),
        businessAPI.getRevenueData(selectedBusiness, selectedPeriod),
        bookingAPI.getChartData(selectedBusiness, selectedPeriod),
        businessAPI.getServiceStats(selectedBusiness),
        customerAPI.getAnalytics(selectedBusiness),
        businessAPI.getRecentActivity(selectedBusiness)
      ]);
      
      if (statsRes.data) stats = statsRes.data;
      else console.error('Stats failed:', statsRes.error);
      
      if (revenueRes.data) revenueData = revenueRes.data;
      else console.error('Revenue failed:', revenueRes.error);
      
      if (bookingsRes.data) bookingData = bookingsRes.data;
      else console.error('Bookings failed:', bookingsRes.error);
      
      if (servicesRes.data) serviceData = servicesRes.data;
      else console.error('Services failed:', servicesRes.error);
      
      if (customersRes.data) customerData = customersRes.data;
      else console.error('Customers failed:', customersRes.error);
      
      if (activitiesRes.data) activities = activitiesRes.data;
      else console.error('Activities failed:', activitiesRes.error);
      
      loading = false;
    }
    
    function handlePeriodChange() {
      loadDashboardData();
    }
    
    function handleBusinessChange() {
      loadDashboardData();
    }
    
    function exportData() {
      toast.success('Exporting dashboard data...');
      // Implement export functionality
    }
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <!-- Dashboard Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p class="mt-1 text-sm text-gray-600">
              Welcome back, {$auth.user?.full_name || 'User'}! Here's your business overview.
            </p>
          </div>
          
          <div class="flex items-center space-x-4">
            {#if businesses.length > 1}
              <Select
                bind:value={selectedBusiness}
                on:change={handleBusinessChange}
                options={businesses.map(b => ({ value: businessAPI.getBusinessIdentifier(b), label: b.name }))}
              />
            {/if}
            
            <Select
              bind:value={selectedPeriod}
              on:change={handlePeriodChange}
              options={periodOptions}
            />
            
            <Button variant="outline" on:click={exportData}>
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Export
            </Button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Stats Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Total Revenue"
          value={stats.revenue}
          change={stats.revenueChange}
          changeType={stats.revenueChange >= 0 ? 'increase' : 'decrease'}
          format="currency"
          icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          color="green"
          {loading}
        />
        
        <StatsCard
          title="Total Bookings"
          value={stats.bookings}
          change={stats.bookingsChange}
          changeType={stats.bookingsChange >= 0 ? 'increase' : 'decrease'}
          icon="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
          color="blue"
          {loading}
        />
        
        <StatsCard
          title="Active Customers"
          value={stats.customers}
          change={stats.customersChange}
          changeType={stats.customersChange >= 0 ? 'increase' : 'decrease'}
          icon="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
          color="purple"
          {loading}
        />
        
        <StatsCard
          title="Average Rating"
          value={stats.rating}
          change={stats.ratingChange}
          changeType={stats.ratingChange >= 0 ? 'increase' : 'decrease'}
          format="decimal"
          icon="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
          color="yellow"
          {loading}
        />
      </div>
      
      <!-- Charts Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <RevenueChart
          data={revenueData}
          {loading}
          period={selectedPeriod}
        />
        
        <BookingChart
          data={bookingData}
          {loading}
        />
        
        <ServiceChart
          data={serviceData}
          {loading}
        />
        
        <CustomerChart
          data={customerData}
          {loading}
        />
      </div>
      
      <!-- Recent Activity -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2">
          {#if businesses.length === 0 && !loading}
            <!-- No Business Welcome Message -->
            <div class="bg-white rounded-lg shadow-sm p-8 text-center">
              <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-indigo-100 mb-4">
                <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-2m-2 0h-2m-2 0h-2M3 5a2 2 0 012-2h10a2 2 0 012 2v16M9 7h1m-1 4h1m-1 4h1m-1 4h1" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">Welcome to Your Dashboard!</h3>
              <p class="text-gray-600 mb-6">
                Get started by creating your first business profile to begin accepting bookings and managing your services.
              </p>
              <Button on:click={() => goto('/businesses/new')}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Create Your First Business
              </Button>
            </div>
          {:else}
            <RecentActivity
              {activities}
              {loading}
            />
          {/if}
        </div>
        
        <!-- Quick Actions -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          {#if businesses.length === 0 && !loading}
            <!-- No Business Quick Actions -->
            <div class="space-y-3">
              <Button fullWidth on:click={() => goto('/businesses/new')}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-2m-2 0h-2m-2 0h-2M3 5a2 2 0 012-2h10a2 2 0 012 2v16M9 7h1m-1 4h1m-1 4h1m-1 4h1" />
                </svg>
                Create Business
              </Button>
              
              <Button fullWidth variant="outline" on:click={() => goto('/businesses')}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                Browse Businesses
              </Button>
              
              <Button fullWidth variant="outline" on:click={() => goto('/subscriptions')}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                View Pricing Plans
              </Button>
            </div>
          {:else}
            <!-- Regular Quick Actions -->
            <div class="space-y-3">
            <Button fullWidth variant="outline" on:click={() => goto('/bookings/new')}>
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              New Booking
            </Button>
            
            {#if selectedBusiness && businesses.find(b => b.id === selectedBusiness)}
              <Button fullWidth variant="outline" on:click={() => {
                const business = businesses.find(b => businessAPI.getBusinessIdentifier(b) === selectedBusiness);
                if (business) {
                  goto(`/businesses/${business.slug}/services/new`);
                }
              }}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Add Service
              </Button>
              
              <Button fullWidth variant="outline" on:click={() => {
                const business = businesses.find(b => businessAPI.getBusinessIdentifier(b) === selectedBusiness);
                if (business) {
                  goto(`/businesses/${business.slug}/services`);
                }
              }}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                Manage Services
              </Button>
            {:else}
              <Button fullWidth variant="outline" disabled>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Add Service
              </Button>
              
              <Button fullWidth variant="outline" disabled>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                Manage Services
              </Button>
            {/if}
            
            <Button fullWidth variant="outline" on:click={() => goto('/customers')}>
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              View Customers
            </Button>
            
            {#if selectedBusiness && businesses.find(b => b.id === selectedBusiness)}
              <Button fullWidth variant="outline" on:click={() => {
                const business = businesses.find(b => businessAPI.getBusinessIdentifier(b) === selectedBusiness);
                if (business) {
                  goto(`/businesses/${business.slug}/analytics`);
                }
              }}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                View Analytics
              </Button>
              
              <Button fullWidth variant="outline" on:click={() => {
                const business = businesses.find(b => businessAPI.getBusinessIdentifier(b) === selectedBusiness);
                if (business) {
                  goto(`/businesses/${business.slug}/edit`);
                }
              }}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Edit Business
              </Button>
            {:else}
              <Button fullWidth variant="outline" disabled>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                View Analytics
              </Button>
              
              <Button fullWidth variant="outline" disabled>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                Edit Business
              </Button>
            {/if}
            
            <Button fullWidth variant="outline" on:click={() => goto('/bookings')}>
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              All Bookings
            </Button>
            </div>
          {/if}
          
          <!-- Help Section -->
          <div class="mt-6 p-4 bg-indigo-50 rounded-lg">
            <h4 class="text-sm font-medium text-indigo-900 mb-2">Need Help?</h4>
            <p class="text-sm text-indigo-700 mb-3">
              Check out our guides to get the most out of your dashboard.
            </p>
            <Button size="sm" variant="outline" on:click={() => toast.info('Help center coming soon!')}>
              View Help Center
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>