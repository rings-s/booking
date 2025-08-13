<!-- src/lib/components/booking/BookingList.svelte -->
<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { bookingStore, bookings } from '$lib/stores/booking';
  import BookingCard from './BookingCard.svelte';
  import Button from '../common/Button.svelte';
  import Select from '../common/Select.svelte';
  import Input from '../common/Input.svelte';
  import Spinner from '../common/Spinner.svelte';
  import Alert from '../common/Alert.svelte';
  import { BOOKING_STATUS } from '$lib/utils/constants';
  import { formatDate } from '$lib/utils/formatters';
  
  export let customerView = false;
  export let businessId = null;
  export let showFilters = true;
  export let showPagination = true;
  export let itemsPerPage = 10;
  export let autoRefresh = false;
  export let refreshInterval = 30000; // 30 seconds
  export let groupByDate = false;
  export let compact = false;
  
  const dispatch = createEventDispatcher();
  
  let loading = true;
  let currentPage = 1;
  let totalPages = 1;
  let totalCount = 0;
  let filteredBookings = [];
  let groupedBookings = {};
  let refreshTimer = null;
  
  let filters = {
    status: '',
    search: '',
    startDate: '',
    endDate: '',
    timeRange: 'all', // all, today, tomorrow, week, month
    sortBy: 'date_desc' // date_desc, date_asc, status, price
  };
  
  // Quick filter presets
  const timeRangeOptions = [
    { value: 'all', label: 'All Time' },
    { value: 'today', label: 'Today' },
    { value: 'tomorrow', label: 'Tomorrow' },
    { value: 'week', label: 'This Week' },
    { value: 'month', label: 'This Month' },
    { value: 'custom', label: 'Custom Range' }
  ];
  
  const sortOptions = [
    { value: 'date_desc', label: 'Newest First' },
    { value: 'date_asc', label: 'Oldest First' },
    { value: 'status', label: 'By Status' },
    { value: 'price', label: 'By Price' }
  ];
  
  onMount(() => {
    loadBookings();
    
    if (autoRefresh) {
      refreshTimer = setInterval(loadBookings, refreshInterval);
    }
    
    return () => {
      if (refreshTimer) {
        clearInterval(refreshTimer);
      }
    };
  });
  
  async function loadBookings() {
    loading = true;
    
    const params = {
      page: currentPage,
      page_size: itemsPerPage,
      ...buildFilterParams()
    };
    
    if (businessId) {
      params.business = businessId;
    }
    
    await bookingStore.loadBookings(params);
    
    const state = $bookings;
    filteredBookings = state.bookings || [];
    totalPages = state.pagination?.totalPages || 1;
    totalCount = state.pagination?.totalCount || 0;
    
    if (groupByDate) {
      groupBookingsByDate();
    }
    
    loading = false;
  }
  
  function buildFilterParams() {
    const params = {};
    
    if (filters.status) {
      params.status = filters.status;
    }
    
    if (filters.search) {
      params.search = filters.search;
    }
    
    // Handle time range filters
    const today = new Date();
    switch (filters.timeRange) {
      case 'today':
        params.booking_date = formatDate(today, 'yyyy-MM-dd');
        break;
      case 'tomorrow':
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        params.booking_date = formatDate(tomorrow, 'yyyy-MM-dd');
        break;
      case 'week':
        params.start_date = formatDate(today, 'yyyy-MM-dd');
        const weekEnd = new Date(today);
        weekEnd.setDate(weekEnd.getDate() + 7);
        params.end_date = formatDate(weekEnd, 'yyyy-MM-dd');
        break;
      case 'month':
        params.start_date = formatDate(today, 'yyyy-MM-dd');
        const monthEnd = new Date(today);
        monthEnd.setMonth(monthEnd.getMonth() + 1);
        params.end_date = formatDate(monthEnd, 'yyyy-MM-dd');
        break;
      case 'custom':
        if (filters.startDate) params.start_date = filters.startDate;
        if (filters.endDate) params.end_date = filters.endDate;
        break;
    }
    
    // Handle sorting
    switch (filters.sortBy) {
      case 'date_asc':
        params.ordering = 'booking_date,start_time';
        break;
      case 'date_desc':
        params.ordering = '-booking_date,-start_time';
        break;
      case 'status':
        params.ordering = 'status,booking_date';
        break;
      case 'price':
        params.ordering = '-total_price';
        break;
    }
    
    return params;
  }
  
  function groupBookingsByDate() {
    groupedBookings = {};
    
    filteredBookings.forEach(booking => {
      const date = booking.booking_date;
      if (!groupedBookings[date]) {
        groupedBookings[date] = [];
      }
      groupedBookings[date].push(booking);
    });
  }
  
  async function handleFilter() {
    currentPage = 1;
    await loadBookings();
  }
  
  async function handlePageChange(page) {
    currentPage = page;
    await loadBookings();
  }
  
  async function handleQuickFilter(timeRange) {
    filters.timeRange = timeRange;
    await handleFilter();
  }
  
  async function handleSort(sortBy) {
    filters.sortBy = sortBy;
    await handleFilter();
  }
  
  async function handleBookingAction(action, booking) {
    dispatch(action, booking);
    
    // Reload bookings after action
    await loadBookings();
  }
  
  function exportBookings() {
    // Create CSV export
    const csv = [
      ['Date', 'Time', 'Service', 'Customer', 'Status', 'Price'],
      ...filteredBookings.map(b => [
        b.booking_date,
        b.start_time,
        b.service.name,
        customerView ? b.business.name : b.customer.user.full_name,
        b.status,
        b.total_price
      ])
    ].map(row => row.join(',')).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `bookings-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }
</script>

<div class="space-y-4">
  <!-- Filters -->
  {#if showFilters}
    <div class="bg-white rounded-lg shadow p-4">
      <!-- Quick Filters -->
      <div class="flex flex-wrap gap-2 mb-4">
        {#each timeRangeOptions as option}
          <Button
            size="sm"
            variant={filters.timeRange === option.value ? 'primary' : 'outline'}
            on:click={() => handleQuickFilter(option.value)}
          >
            {option.label}
          </Button>
        {/each}
      </div>
      
      <!-- Advanced Filters -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Input
          type="search"
          placeholder="Search bookings..."
          bind:value={filters.search}
          on:input={handleFilter}
        />
        
        <Select
          placeholder="All Status"
          bind:value={filters.status}
          on:change={handleFilter}
          options={[
            { value: '', label: 'All Status' },
            ...Object.entries(BOOKING_STATUS).map(([key, value]) => ({
              value: value,
              label: key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' ')
            }))
          ]}
        />
        
        <Select
          placeholder="Sort By"
          bind:value={filters.sortBy}
          on:change={handleFilter}
          options={sortOptions}
        />
        
        <Button variant="outline" on:click={exportBookings}>
          <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Export
        </Button>
      </div>
      
      {#if filters.timeRange === 'custom'}
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
          <Input
            type="date"
            label="From Date"
            bind:value={filters.startDate}
            on:change={handleFilter}
          />
          
          <Input
            type="date"
            label="To Date"
            bind:value={filters.endDate}
            on:change={handleFilter}
          />
        </div>
      {/if}
    </div>
  {/if}
  
  <!-- Stats Bar -->
  {#if !loading && totalCount > 0}
    <div class="bg-white rounded-lg shadow p-4">
      <div class="flex items-center justify-between">
        <p class="text-sm text-gray-600">
          Showing {Math.min((currentPage - 1) * itemsPerPage + 1, totalCount)} to {Math.min(currentPage * itemsPerPage, totalCount)} of {totalCount} bookings
        </p>
        
        {#if autoRefresh}
          <div class="flex items-center text-sm text-gray-500">
            <svg class="animate-spin h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Auto-refreshing
          </div>
        {/if}
      </div>
    </div>
  {/if}
  
  <!-- Bookings List -->
  {#if loading}
    <div class="flex justify-center py-12">
      <Spinner size="lg">Loading bookings...</Spinner>
    </div>
  {:else if filteredBookings.length > 0}
    {#if groupByDate}
      <!-- Grouped by Date -->
      {#each Object.entries(groupedBookings) as [date, dateBookings]}
        <div class="space-y-4">
          <div class="flex items-center">
            <h3 class="text-lg font-semibold text-gray-900">
              {formatDate(date, 'EEEE, MMMM d, yyyy')}
            </h3>
            <span class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
              {dateBookings.length} bookings
            </span>
          </div>
          
          <div class="space-y-3">
            {#each dateBookings as booking}
              <BookingCard
                {booking}
                {customerView}
                {compact}
                showActions={!compact}
                on:cancelled={({ detail }) => handleBookingAction('cancelled', detail)}
                on:confirmed={({ detail }) => handleBookingAction('confirmed', detail)}
                on:completed={({ detail }) => handleBookingAction('completed', detail)}
                on:noshow={({ detail }) => handleBookingAction('noshow', detail)}
              />
            {/each}
          </div>
        </div>
      {/each}
    {:else}
      <!-- Regular List -->
      <div class="space-y-3">
        {#each filteredBookings as booking}
          <BookingCard
            {booking}
            {customerView}
            {compact}
            showActions={!compact}
            on:cancelled={({ detail }) => handleBookingAction('cancelled', detail)}
            on:confirmed={({ detail }) => handleBookingAction('confirmed', detail)}
            on:completed={({ detail }) => handleBookingAction('completed', detail)}
            on:noshow={({ detail }) => handleBookingAction('noshow', detail)}
          />
        {/each}
      </div>
    {/if}
    
    <!-- Pagination -->
    {#if showPagination && totalPages > 1}
      <div class="flex items-center justify-between">
        <Button
          variant="outline"
          size="sm"
          disabled={currentPage === 1}
          on:click={() => handlePageChange(currentPage - 1)}
        >
          <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Previous
        </Button>
        
        <div class="flex items-center space-x-2">
          {#each Array(Math.min(5, totalPages)) as _, i}
            {@const page = currentPage <= 3 ? i + 1 : currentPage + i - 2}
            {#if page > 0 && page <= totalPages}
              <button
                type="button"
                class="
                  px-3 py-1 text-sm rounded-md
                  {page === currentPage 
                    ? 'bg-indigo-600 text-white' 
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'}
                "
                on:click={() => handlePageChange(page)}
              >
                {page}
              </button>
            {/if}
          {/each}
        </div>
        
        <Button
          variant="outline"
          size="sm"
          disabled={currentPage === totalPages}
          on:click={() => handlePageChange(currentPage + 1)}
        >
          Next
          <svg class="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </Button>
      </div>
    {/if}
  {:else}
    <!-- Empty State -->
    <div class="bg-white rounded-lg shadow p-12 text-center">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <h3 class="mt-2 text-sm font-medium text-gray-900">No bookings found</h3>
      <p class="mt-1 text-sm text-gray-500">
        {filters.search || filters.status || filters.timeRange !== 'all' 
          ? 'Try adjusting your filters' 
          : customerView 
            ? 'You haven\'t made any bookings yet' 
            : 'You don\'t have any bookings yet'}
      </p>
      <div class="mt-6">
        {#if filters.search || filters.status || filters.timeRange !== 'all'}
          <Button on:click={() => { filters = { status: '', search: '', startDate: '', endDate: '', timeRange: 'all', sortBy: 'date_desc' }; handleFilter(); }}>
            Clear Filters
          </Button>
        {:else if customerView}
          <Button href="/businesses">Browse Services</Button>
        {/if}
      </div>
    </div>
  {/if}
</div>