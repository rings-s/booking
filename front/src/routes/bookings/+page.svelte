<!-- src/routes/bookings/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { bookingAPI } from '$lib/api/bookings';
    import { auth } from '$lib/stores/auth';
    import BookingCard from '$lib/components/booking/BookingCard.svelte';
    import BookingStatus from '$lib/components/booking/BookingStatus.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Select from '$lib/components/common/Select.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import Pagination from '$lib/components/common/Pagination.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import toast from 'svelte-french-toast';
    
    let bookings = [];
    let loading = true;
    let view = 'list'; // 'list', 'calendar', 'grid'
    let filterStatus = '';
    let filterDate = '';
    let searchQuery = '';
    let sortBy = 'date_desc';
    let currentPage = 1;
    let totalPages = 1;
    let totalBookings = 0;
    let selectedBooking = null;
    let showCancelModal = false;
    let cancelling = false;
    
    // Calendar view
    let currentMonth = new Date();
    let calendarBookings = {};
    
    const statusOptions = [
      { value: '', label: 'All Status' },
      { value: 'pending', label: 'Pending' },
      { value: 'confirmed', label: 'Confirmed' },
      { value: 'completed', label: 'Completed' },
      { value: 'cancelled', label: 'Cancelled' },
      { value: 'no_show', label: 'No Show' }
    ];
    
    const sortOptions = [
      { value: 'date_desc', label: 'Newest First' },
      { value: 'date_asc', label: 'Oldest First' },
      { value: 'status', label: 'By Status' },
      { value: 'service', label: 'By Service' },
      { value: 'amount', label: 'By Amount' }
    ];
    
    onMount(async () => {
      await loadBookings();
    });
    
    async function loadBookings() {
      loading = true;
      
      const params = {
        page: currentPage,
        status: filterStatus,
        date: filterDate,
        search: searchQuery,
        sort: sortBy
      };
      
      const { data, error } = await bookingAPI.list(params);
      
      if (data) {
        bookings = data.results;
        totalPages = data.total_pages;
        totalBookings = data.count;
        
        if (view === 'calendar') {
          organizeBookingsForCalendar();
        }
      } else if (error) {
        toast.error('Failed to load bookings');
      }
      
      loading = false;
    }
    
    function organizeBookingsForCalendar() {
      calendarBookings = {};
      bookings.forEach(booking => {
        const date = new Date(booking.booking_date).toDateString();
        if (!calendarBookings[date]) {
          calendarBookings[date] = [];
        }
        calendarBookings[date].push(booking);
      });
    }
    
    async function handleStatusUpdate(booking, newStatus) {
      const { data, error } = await bookingAPI.updateStatus(booking.id, newStatus);
      
      if (data) {
        const index = bookings.findIndex(b => b.id === booking.id);
        bookings[index] = data;
        toast.success(`Booking ${newStatus}`);
      } else {
        toast.error('Failed to update booking status');
      }
    }
    
    async function handleCancel() {
      if (!selectedBooking) return;
      
      cancelling = true;
      const { data, error } = await bookingAPI.cancel(selectedBooking.id);
      
      if (data) {
        const index = bookings.findIndex(b => b.id === selectedBooking.id);
        bookings[index] = data;
        showCancelModal = false;
        selectedBooking = null;
        toast.success('Booking cancelled successfully');
      } else {
        toast.error('Failed to cancel booking');
      }
      
      cancelling = false;
    }
    
    function handleSearch() {
      currentPage = 1;
      loadBookings();
    }
    
    function handleFilterChange() {
      currentPage = 1;
      loadBookings();
    }
    
    function getDaysInMonth(date) {
      const year = date.getFullYear();
      const month = date.getMonth();
      const firstDay = new Date(year, month, 1);
      const lastDay = new Date(year, month + 1, 0);
      const daysInMonth = lastDay.getDate();
      const startingDayOfWeek = firstDay.getDay();
      
      const days = [];
      
      // Add empty cells for days before month starts
      for (let i = 0; i < startingDayOfWeek; i++) {
        days.push(null);
      }
      
      // Add days of the month
      for (let i = 1; i <= daysInMonth; i++) {
        days.push(new Date(year, month, i));
      }
      
      return days;
    }
    
    function previousMonth() {
      currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1);
      loadBookings();
    }
    
    function nextMonth() {
      currentMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1);
      loadBookings();
    }
    
    // Get booking stats
    $: pendingCount = bookings.filter(b => b.status === 'pending').length;
    $: todayCount = bookings.filter(b => {
      const today = new Date().toDateString();
      return new Date(b.booking_date).toDateString() === today;
    }).length;
    $: upcomingCount = bookings.filter(b => {
      return new Date(b.booking_date) > new Date() && b.status !== 'cancelled';
    }).length;
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Bookings</h1>
            <p class="mt-1 text-sm text-gray-600">
              Manage all your appointments and reservations
            </p>
          </div>
          
          <Button href="/bookings/new">
            <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            New Booking
          </Button>
        </div>
      </div>
    </div>
    
    <!-- Quick Stats -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Today</p>
              <p class="text-2xl font-bold text-gray-900">{todayCount}</p>
            </div>
            <div class="p-3 bg-blue-100 rounded-lg">
              <svg class="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        </Card>
        
        <Card>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Pending</p>
              <p class="text-2xl font-bold text-yellow-600">{pendingCount}</p>
            </div>
            <div class="p-3 bg-yellow-100 rounded-lg">
              <svg class="w-6 h-6 text-yellow-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </Card>
        
        <Card>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Upcoming</p>
              <p class="text-2xl font-bold text-green-600">{upcomingCount}</p>
            </div>
            <div class="p-3 bg-green-100 rounded-lg">
              <svg class="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
        </Card>
        
        <Card>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Total</p>
              <p class="text-2xl font-bold text-gray-900">{totalBookings}</p>
            </div>
            <div class="p-3 bg-indigo-100 rounded-lg">
              <svg class="w-6 h-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
          </div>
        </Card>
      </div>
    </div>
    
    <!-- Filters and View Toggle -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <Card>
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div class="flex flex-wrap items-center gap-3">
            <!-- Search -->
            <div class="w-64">
              <Input
                type="search"
                placeholder="Search bookings..."
                bind:value={searchQuery}
                on:input={handleSearch}
              />
            </div>
            
            <!-- Status Filter -->
            <Select
              bind:value={filterStatus}
              options={statusOptions}
              on:change={handleFilterChange}
            />
            
            <!-- Date Filter -->
            <Input
              type="date"
              bind:value={filterDate}
              on:change={handleFilterChange}
            />
            
            <!-- Sort -->
            <Select
              bind:value={sortBy}
              options={sortOptions}
              on:change={handleFilterChange}
            />
          </div>
          
          <!-- View Toggle -->
          <div class="flex items-center bg-gray-100 rounded-lg p-1">
            {#each [
              { value: 'list', icon: 'M4 6h16M4 12h16M4 18h16' },
              { value: 'grid', icon: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z' },
              { value: 'calendar', icon: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' }
            ] as option}
              <button
                class="px-3 py-2 rounded-md transition-colors {view === option.value ? 'bg-white shadow-sm' : 'hover:bg-gray-200'}"
                on:click={() => {
                  view = option.value;
                  if (option.value === 'calendar') {
                    organizeBookingsForCalendar();
                  }
                }}
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={option.icon} />
                </svg>
              </button>
            {/each}
          </div>
        </div>
      </Card>
    </div>
    
    <!-- Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {#if loading}
        <div class="flex justify-center py-12">
          <Spinner size="lg">Loading bookings...</Spinner>
        </div>
      {:else if bookings.length === 0}
        <Card>
          <div class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <h3 class="mt-2 text-lg font-medium text-gray-900">No bookings found</h3>
            <p class="mt-1 text-sm text-gray-500">
              {searchQuery || filterStatus || filterDate 
                ? 'Try adjusting your filters' 
                : 'Get started by creating your first booking'}
            </p>
            <div class="mt-6">
              {#if searchQuery || filterStatus || filterDate}
                <Button variant="outline" on:click={() => {
                  searchQuery = '';
                  filterStatus = '';
                  filterDate = '';
                  handleFilterChange();
                }}>
                  Clear Filters
                </Button>
              {:else}
                <Button href="/bookings/new">
                  Create Booking
                </Button>
              {/if}
            </div>
          </div>
        </Card>
      {:else if view === 'calendar'}
        <!-- Calendar View -->
        <Card>
          <div slot="header" class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900">
              {currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
            </h3>
            <div class="flex items-center space-x-2">
              <button
                class="p-2 hover:bg-gray-100 rounded-lg"
                on:click={previousMonth}
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                class="px-3 py-1 text-sm font-medium bg-indigo-100 text-indigo-700 rounded-lg"
                on:click={() => currentMonth = new Date()}
              >
                Today
              </button>
              <button
                class="p-2 hover:bg-gray-100 rounded-lg"
                on:click={nextMonth}
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="grid grid-cols-7 gap-px bg-gray-200">
            <!-- Week days header -->
            {#each ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] as day}
              <div class="bg-gray-50 px-2 py-3 text-center text-xs font-medium text-gray-700">
                {day}
              </div>
            {/each}
            
            <!-- Calendar days -->
            {#each getDaysInMonth(currentMonth) as day}
              {#if day}
                {@const dateStr = day.toDateString()}
                {@const dayBookings = calendarBookings[dateStr] || []}
                {@const isToday = dateStr === new Date().toDateString()}
                
                <div class="bg-white min-h-[100px] p-2 {isToday ? 'bg-indigo-50' : ''}">
                  <div class="text-sm font-medium text-gray-900 mb-1">
                    {day.getDate()}
                  </div>
                  
                  {#if dayBookings.length > 0}
                    <div class="space-y-1">
                      {#each dayBookings.slice(0, 3) as booking}
                        <button
                          class="w-full text-left px-1 py-0.5 text-xs rounded truncate
                            {booking.status === 'confirmed' ? 'bg-green-100 text-green-700' : ''}
                            {booking.status === 'pending' ? 'bg-yellow-100 text-yellow-700' : ''}
                            {booking.status === 'cancelled' ? 'bg-red-100 text-red-700 line-through' : ''}"
                          on:click={() => goto(`/bookings/${booking.id}`)}
                        >
                          {booking.start_time} - {booking.customer.user.full_name}
                        </button>
                      {/each}
                      
                      {#if dayBookings.length > 3}
                        <div class="text-xs text-gray-500 text-center">
                          +{dayBookings.length - 3} more
                        </div>
                      {/if}
                    </div>
                  {/if}
                </div>
              {:else}
                <div class="bg-gray-50"></div>
              {/if}
            {/each}
          </div>
        </Card>
      {:else if view === 'grid'}
        <!-- Grid View -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {#each bookings as booking}
            <Card>
              <div class="space-y-3">
                <div class="flex items-start justify-between">
                  <div>
                    <h3 class="font-semibold text-gray-900">
                      {booking.service.name}
                    </h3>
                    <p class="text-sm text-gray-600">
                      {booking.business.name}
                    </p>
                  </div>
                  <BookingStatus status={booking.status} size="sm" />
                </div>
                
                <div class="space-y-2 text-sm">
                  <div class="flex items-center text-gray-600">
                    <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    {booking.customer.user.full_name}
                  </div>
                  
                  <div class="flex items-center text-gray-600">
                    <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {new Date(booking.booking_date).toLocaleDateString()}
                  </div>
                  
                  <div class="flex items-center text-gray-600">
                    <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    {booking.start_time} - {booking.end_time}
                  </div>
                  
                  <div class="flex items-center font-semibold text-gray-900">
                    <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    ${booking.total_price}
                  </div>
                </div>
                
                <div class="flex gap-2 pt-3 border-t border-gray-200">
                  <Button
                    size="sm"
                    variant="outline"
                    href="/bookings/{booking.id}"
                    class="flex-1"
                  >
                    View
                  </Button>
                  
                  {#if booking.status === 'pending'}
                    <Button
                      size="sm"
                      on:click={() => handleStatusUpdate(booking, 'confirmed')}
                      class="flex-1"
                    >
                      Confirm
                    </Button>
                  {:else if booking.status === 'confirmed' && new Date(booking.booking_date) > new Date()}
                    <Button
                      size="sm"
                      variant="outline"
                      on:click={() => {
                        selectedBooking = booking;
                        showCancelModal = true;
                      }}
                      class="flex-1"
                    >
                      Cancel
                    </Button>
                  {/if}
                </div>
              </div>
            </Card>
          {/each}
        </div>
      {:else}
        <!-- List View -->
        <Card>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Booking
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date & Time
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                  <th class="relative px-6 py-3">
                    <span class="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                {#each bookings as booking}
                  <tr class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div class="text-sm font-medium text-gray-900">
                          {booking.service.name}
                        </div>
                        <div class="text-sm text-gray-500">
                          {booking.business.name}
                        </div>
                      </div>
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <div class="flex-shrink-0 h-10 w-10">
                          <div class="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center">
                            <span class="text-sm font-medium text-indigo-600">
                              {booking.customer.user.full_name.split(' ').map(n => n[0]).join('')}
                            </span>
                          </div>
                        </div>
                        <div class="ml-4">
                          <div class="text-sm font-medium text-gray-900">
                            {booking.customer.user.full_name}
                          </div>
                          <div class="text-sm text-gray-500">
                            {booking.customer.user.email}
                          </div>
                        </div>
                      </div>
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-900">
                        {new Date(booking.booking_date).toLocaleDateString()}
                      </div>
                      <div class="text-sm text-gray-500">
                        {booking.start_time} - {booking.end_time}
                      </div>
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap">
                      <BookingStatus status={booking.status} />
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      ${booking.total_price}
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div class="flex items-center justify-end space-x-2">
                        <Button
                          size="sm"
                          variant="outline"
                          href="/bookings/{booking.id}"
                        >
                          View
                        </Button>
                        
                        {#if booking.status === 'pending'}
                          <Button
                            size="sm"
                            on:click={() => handleStatusUpdate(booking, 'confirmed')}
                          >
                            Confirm
                          </Button>
                        {/if}
                      </div>
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </Card>
      {/if}
      
      <!-- Pagination -->
      {#if !loading && totalPages > 1 && view !== 'calendar'}
        <div class="mt-6">
          <Pagination
            bind:currentPage
            {totalPages}
            on:change={loadBookings}
          />
        </div>
      {/if}
    </div>
    
    <!-- Cancel Modal -->
    <Modal bind:open={showCancelModal} title="Cancel Booking" size="md">
      <p class="text-gray-600">
        Are you sure you want to cancel this booking? This action cannot be undone.
      </p>
      
      {#if selectedBooking}
        <div class="mt-4 p-4 bg-gray-50 rounded-lg">
          <dl class="space-y-2 text-sm">
            <div class="flex justify-between">
              <dt class="text-gray-600">Service:</dt>
              <dd class="font-medium text-gray-900">{selectedBooking.service.name}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-gray-600">Customer:</dt>
              <dd class="font-medium text-gray-900">{selectedBooking.customer.user.full_name}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-gray-600">Date:</dt>
              <dd class="font-medium text-gray-900">
                {new Date(selectedBooking.booking_date).toLocaleDateString()}
              </dd>
            </div>
          </dl>
        </div>
      {/if}
      
      <div slot="footer" class="flex justify-end gap-3">
        <Button variant="outline" on:click={() => showCancelModal = false}>
          Keep Booking
        </Button>
        <Button variant="danger" on:click={handleCancel} loading={cancelling}>
          Cancel Booking
        </Button>
      </div>
    </Modal>
  </div>