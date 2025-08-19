<!-- src/routes/dashboard/+page.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import { goto } from '$app/navigation';
    import { auth, isAuthenticated, canManageBusinesses } from '$lib/stores/auth';
    import { 
        dashboard, 
        loading, 
        error, 
        activePeriod, 
        statsData, 
        revenueData, 
        bookingChartData, 
        serviceStats, 
        recentActivity,
        popularServices,
        customerMetrics,
        bookingTrends,
        revenueTrends,
        initDashboard,
        changeDashboardPeriod,
        clearDashboard
    } from '$lib/stores/dashboard';
    import { businessAPI } from '$lib/api/businesses';
    import StatsCard from '$lib/components/dashboard/StatsCard.svelte';
    import RevenueChart from '$lib/components/dashboard/RevenueChart.svelte';
    import BookingChart from '$lib/components/dashboard/BookingChart.svelte';
    import ServiceChart from '$lib/components/dashboard/ServiceChart.svelte';
    import CustomerChart from '$lib/components/dashboard/CustomerChart.svelte';
    import RecentActivity from '$lib/components/dashboard/RecentActivity.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Select from '$lib/components/common/Select.svelte';
    import { t } from '$lib/stores/i18n.js';
    import toast from 'svelte-french-toast';
    
    let selectedBusiness = null;
    let businesses = [];
    
    $: periodOptions = [
      { value: 'week', label: $t('time.this_week') },
      { value: 'month', label: $t('time.this_month') },
      { value: 'quarter', label: $t('time.this_quarter') },
      { value: 'year', label: $t('time.this_year') }
    ];
    
    onMount(async () => {
      // Wait for auth to be initialized
      if ($auth.isLoading) {
        const unsubscribe = auth.subscribe((authState) => {
          if (!authState.isLoading) {
            unsubscribe();
            checkAuthAndLoadData();
          }
        });
      } else {
        await checkAuthAndLoadData();
      }
    });

    onDestroy(() => {
      // Clear dashboard data on component destruction
      clearDashboard();
    });
    
    async function checkAuthAndLoadData() {
      // Redirect to login if not authenticated
      if (!$isAuthenticated) {
        toast.error($t('auth.please_sign_in_dashboard'));
        goto('/auth/login');
        return;
      }
      
      // Check if user can manage businesses (business owner, staff, or superuser)
      if (!$canManageBusinesses) {
        console.log('Access check failed:', {
          user: $auth.user,
          isAuthenticated: $isAuthenticated,
          canManageBusinesses: $canManageBusinesses,
          isStaff: $auth.user?.is_staff,
          isSuperuser: $auth.user?.is_superuser,
          userType: $auth.user?.user_type
        });
        toast.error($t('auth.access_denied_business_permissions'));
        goto('/');
        return;
      }
      
      await loadBusinesses();
      
      if (selectedBusiness) {
        console.log('Dashboard: Initial data load for business:', selectedBusiness);
        await initDashboard(selectedBusiness);
        console.log('Dashboard: Initial data loaded, checking chart data:', {
          bookingTrendsDaily: $bookingTrends.daily?.length,
          revenueTrendsMonthly: $revenueTrends.monthly?.length, 
          popularServicesCount: $popularServices?.length,
          loading: $loading
        });
      }
    }
    
    async function loadBusinesses() {
      // Load businesses owned by the current user (regardless of admin status)
      // Dashboard is for managing your own businesses, not all businesses in the system
      const { data, error } = await businessAPI.getMyBusinesses();
      
      if (data) {
        // getMyBusinesses returns an array directly
        businesses = Array.isArray(data) ? data : (data.results || []);
        
        if (businesses.length > 0) {
          selectedBusiness = businessAPI.getBusinessIdentifier(businesses[0]); // Use slug for API calls
        } else {
          selectedBusiness = null;
        }
      } else {
        businesses = [];
        selectedBusiness = null;
        if (error) {
          console.error('Failed to load businesses:', error);
          toast.error($t('error.failed_load_businesses'));
        }
      }
    }
    
    async function handlePeriodChange() {
      await changeDashboardPeriod($activePeriod);
    }
    
    async function handleBusinessChange() {
      if (selectedBusiness) {
        console.log('Dashboard: Loading data for business:', selectedBusiness);
        await initDashboard(selectedBusiness);
        console.log('Dashboard: Data loaded, store values:', {
          bookingTrends: $bookingTrends,
          revenueTrends: $revenueTrends,
          popularServices: $popularServices,
          loading: $loading
        });
      }
    }
    
    function exportData() {
      toast.success($t('dashboard.exporting_data'));
      // Implement export functionality
    }
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <!-- Dashboard Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{$t('navigation.dashboard')}</h1>
            <p class="mt-1 text-sm text-gray-600">
              {$t('dashboard.welcome_back', { name: $auth.user?.full_name || $t('common.user') })}
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
              bind:value={$activePeriod}
              on:change={handlePeriodChange}
              options={periodOptions}
            />
            
            <Button variant="outline" on:click={exportData}>
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              {$t('common.export')}
            </Button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Stats Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title={$t('dashboard.total_revenue')}
          value={$statsData.revenue}
          change={$statsData.revenueChange}
          changeType={$statsData.revenueChange >= 0 ? 'increase' : 'decrease'}
          format="currency"
          icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          color="green"
          loading={$loading}
        />
        
        <StatsCard
          title={$t('dashboard.total_bookings')}
          value={$statsData.bookings}
          change={$statsData.bookingsChange}
          changeType={$statsData.bookingsChange >= 0 ? 'increase' : 'decrease'}
          icon="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
          color="blue"
          loading={$loading}
        />
        
        <StatsCard
          title={$t('dashboard.active_customers')}
          value={$statsData.customers}
          change={$statsData.customersChange}
          changeType={$statsData.customersChange >= 0 ? 'increase' : 'decrease'}
          icon="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
          color="purple"
          loading={$loading}
        />
        
        <StatsCard
          title={$t('dashboard.average_rating')}
          value={$statsData.rating}
          change={$statsData.ratingChange}
          changeType={$statsData.ratingChange >= 0 ? 'increase' : 'decrease'}
          format="decimal"
          icon="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
          color="yellow"
          loading={$loading}
        />
      </div>
      
      <!-- Charts Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <RevenueChart
          data={$revenueTrends.monthly}
          loading={$loading}
          period={$activePeriod}
        />
        
        <BookingChart
          data={$bookingTrends.daily}
          loading={$loading}
        />
        
        <ServiceChart
          data={$popularServices}
          loading={$loading}
        />
        
        <CustomerChart
          data={$customerMetrics}
          loading={$loading}
        />
      </div>
      
      <!-- Recent Activity -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2">
          {#if businesses.length === 0 && !$loading}
            <!-- No Business Welcome Message -->
            <div class="bg-white rounded-lg shadow-sm p-8 text-center">
              <div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-indigo-100 mb-4">
                <svg class="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-2m-2 0h-2m-2 0h-2M3 5a2 2 0 012-2h10a2 2 0 012 2v16M9 7h1m-1 4h1m-1 4h1m-1 4h1" />
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">
                {#if $auth.user?.is_staff || $auth.user?.is_superuser}
                  {$t('dashboard.admin_dashboard')}
                {:else}
                  {$t('dashboard.welcome_to_dashboard')}
                {/if}
              </h3>
              <p class="text-gray-600 mb-6">
                {#if $auth.user?.is_staff || $auth.user?.is_superuser}
                  {$t('dashboard.no_businesses_admin')}
                {:else}
                  {$t('dashboard.get_started_message')}
                {/if}
              </p>
              <Button on:click={() => goto('/businesses/new')}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                {#if $auth.user?.is_staff || $auth.user?.is_superuser}
                  {$t('business.create_new_business')}
                {:else}
                  {$t('business.create_first_business')}
                {/if}
              </Button>
            </div>
          {:else}
            <RecentActivity
              activities={$recentActivity}
              loading={$loading}
            />
          {/if}
        </div>
        
        <!-- Quick Actions -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">{$t('dashboard.quick_actions')}</h3>
          {#if businesses.length === 0 && !$loading}
            <!-- No Business Quick Actions -->
            <div class="space-y-3">
              <Button fullWidth on:click={() => goto('/businesses/new')}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-2m-2 0h-2m-2 0h-2M3 5a2 2 0 012-2h10a2 2 0 012 2v16M9 7h1m-1 4h1m-1 4h1m-1 4h1" />
                </svg>
                {#if $auth.user?.is_staff || $auth.user?.is_superuser}
                  {$t('business.create_new_business')}
                {:else}
                  {$t('business.create_business')}
                {/if}
              </Button>
              
              <Button fullWidth variant="outline" on:click={() => goto('/businesses')}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                {$t('business.browse_businesses')}
              </Button>
              
              {#if !($auth.user?.is_staff || $auth.user?.is_superuser)}
                <Button fullWidth variant="outline" on:click={() => goto('/subscriptions')}>
                  <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {$t('subscription.view_pricing_plans')}
                </Button>
              {:else}
                <Button fullWidth variant="outline" on:click={() => goto('/customers')}>
                  <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  {$t('customer.manage_customers')}
                </Button>
              {/if}
            </div>
          {:else}
            <!-- Regular Quick Actions -->
            <div class="space-y-3">
            <Button fullWidth variant="outline" on:click={() => goto('/bookings/new')}>
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              {$t('booking.new_booking')}
            </Button>
            
            {#if selectedBusiness && businesses.find(b => businessAPI.getBusinessIdentifier(b) === selectedBusiness)}
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
            
            {#if selectedBusiness && businesses.find(b => businessAPI.getBusinessIdentifier(b) === selectedBusiness)}
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