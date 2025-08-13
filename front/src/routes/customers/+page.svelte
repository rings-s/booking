<!-- src/routes/customers/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { customerAPI } from '$lib/api/customers';
    import { bookingAPI } from '$lib/api/bookings';
    import { auth } from '$lib/stores/auth';
    import Avatar from '$lib/components/common/Avatar.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import Select from '$lib/components/common/Select.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import Pagination from '$lib/components/common/Pagination.svelte';
    import toast from 'svelte-french-toast';
    
    let customers = [];
    let loading = true;
    let searchQuery = '';
    let sortBy = 'recent';
    let filterStatus = '';
    let currentPage = 1;
    let totalPages = 1;
    let totalCustomers = 0;
    let selectedCustomer = null;
    let showDetailsModal = false;
    let showNewCustomerModal = false;
    let showImportModal = false;
    let customerStats = {};
    
    // New customer form
    let newCustomer = {
      full_name: '',
      email: '',
      phone: '',
      date_of_birth: '',
      address: '',
      notes: '',
      tags: []
    };
    
    const sortOptions = [
      { value: 'recent', label: 'Most Recent' },
      { value: 'name', label: 'Name (A-Z)' },
      { value: 'bookings', label: 'Most Bookings' },
      { value: 'spending', label: 'Highest Spending' },
      { value: 'last_visit', label: 'Last Visit' }
    ];
    
    const statusOptions = [
      { value: '', label: 'All Customers' },
      { value: 'active', label: 'Active' },
      { value: 'inactive', label: 'Inactive' },
      { value: 'vip', label: 'VIP' },
      { value: 'new', label: 'New (< 30 days)' }
    ];
    
    const tagOptions = [
      'VIP',
      'Regular',
      'First Time',
      'Birthday Month',
      'Referral',
      'Corporate',
      'Student',
      'Senior'
    ];
    
    onMount(async () => {
      await loadCustomers();
      await loadStats();
    });
    
    async function loadCustomers() {
      loading = true;
      
      const params = {
        page: currentPage,
        search: searchQuery,
        sort: sortBy,
        status: filterStatus
      };
      
      const { data, error } = await customerAPI.getAll(params);
      
      if (data) {
        customers = data.results;
        totalPages = data.total_pages;
        totalCustomers = data.count;
      } else if (error) {
        toast.error('Failed to load customers');
      }
      
      loading = false;
    }
    
    async function loadStats() {
      const { data } = await customerAPI.getStats();
      if (data) {
        customerStats = data;
      }
    }
    
    async function loadCustomerDetails(customer) {
      selectedCustomer = customer;
      
      // Load additional details
      const [bookingsRes, statsRes] = await Promise.all([
        bookingAPI.getByCustomer(customer.id, { limit: 5 }),
        customerAPI.getCustomerStats(customer.id)
      ]);
      
      if (bookingsRes.data) {
        selectedCustomer.recent_bookings = bookingsRes.data;
      }
      
      if (statsRes.data) {
        selectedCustomer.stats = statsRes.data;
      }
      
      showDetailsModal = true;
    }
    
    async function handleCreateCustomer() {
      const { data, error } = await customerAPI.create(newCustomer);
      
      if (data) {
        customers = [data, ...customers];
        totalCustomers++;
        showNewCustomerModal = false;
        resetNewCustomerForm();
        toast.success('Customer created successfully');
      } else {
        toast.error(error || 'Failed to create customer');
      }
    }
    
    async function handleDeleteCustomer(customerId) {
      if (!confirm('Are you sure you want to delete this customer?')) return;
      
      const { data, error } = await customerAPI.delete(customerId);
      
      if (data) {
        customers = customers.filter(c => c.id !== customerId);
        totalCustomers--;
        toast.success('Customer deleted successfully');
      } else {
        toast.error('Failed to delete customer');
      }
    }
    
    async function handleExport() {
      const { data, error } = await customerAPI.export({ format: 'csv' });
      
      if (data) {
        const blob = new Blob([data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `customers-${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
        
        toast.success('Customers exported successfully');
      }
    }
    
    async function handleImport(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      const formData = new FormData();
      formData.append('file', file);
      
      const { data, error } = await customerAPI.import(formData);
      
      if (data) {
        await loadCustomers();
        showImportModal = false;
        toast.success(`${data.imported} customers imported successfully`);
      } else {
        toast.error(error || 'Failed to import customers');
      }
    }
    
    function resetNewCustomerForm() {
      newCustomer = {
        full_name: '',
        email: '',
        phone: '',
        date_of_birth: '',
        address: '',
        notes: '',
        tags: []
      };
    }
    
    function handleSearch() {
      currentPage = 1;
      loadCustomers();
    }
    
    function toggleTag(tag) {
      if (newCustomer.tags.includes(tag)) {
        newCustomer.tags = newCustomer.tags.filter(t => t !== tag);
      } else {
        newCustomer.tags = [...newCustomer.tags, tag];
      }
    }
    
    function sendMessage(customer) {
      goto(`/notifications/compose?customer=${customer.id}`);
    }
    
    // Calculate customer metrics
    $: activeCustomers = customerStats.active || 0;
    $: newCustomers = customerStats.new_this_month || 0;
    $: averageLifetimeValue = customerStats.average_lifetime_value || 0;
    $: retentionRate = customerStats.retention_rate || 0;
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Customers</h1>
            <p class="mt-1 text-sm text-gray-600">
              Manage your customer relationships
            </p>
          </div>
          
          <div class="flex items-center space-x-3">
            <Button variant="outline" on:click={handleExport}>
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Export
            </Button>
            
            <Button variant="outline" on:click={() => showImportModal = true}>
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              Import
            </Button>
            
            <Button on:click={() => showNewCustomerModal = true}>
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Add Customer
            </Button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Stats Cards -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Total Customers</p>
              <p class="text-2xl font-bold text-gray-900">{totalCustomers}</p>
            </div>
            <div class="p-3 bg-indigo-100 rounded-lg">
              <svg class="w-6 h-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
          </div>
        </Card>
        
        <Card>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Active Customers</p>
              <p class="text-2xl font-bold text-green-600">{activeCustomers}</p>
            </div>
            <div class="p-3 bg-green-100 rounded-lg">
              <svg class="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </Card>
        
        <Card>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">New This Month</p>
              <p class="text-2xl font-bold text-blue-600">{newCustomers}</p>
            </div>
            <div class="p-3 bg-blue-100 rounded-lg">
              <svg class="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </div>
          </div>
        </Card>
        
        <Card>
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-600">Avg. Lifetime Value</p>
              <p class="text-2xl font-bold text-purple-600">${averageLifetimeValue}</p>
            </div>
            <div class="p-3 bg-purple-100 rounded-lg">
              <svg class="w-6 h-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </Card>
      </div>
    </div>
    
    <!-- Filters -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <Card>
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="flex flex-wrap items-center gap-3">
            <div class="w-64">
              <Input
                type="search"
                placeholder="Search customers..."
                bind:value={searchQuery}
                on:input={handleSearch}
              />
            </div>
            
            <Select
              bind:value={filterStatus}
              options={statusOptions}
              on:change={loadCustomers}
            />
            
            <Select
              bind:value={sortBy}
              options={sortOptions}
              on:change={loadCustomers}
            />
          </div>
          
          <p class="text-sm text-gray-600">
            Showing {customers.length} of {totalCustomers} customers
          </p>
        </div>
      </Card>
    </div>
    
    <!-- Customers Table -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {#if loading}
        <div class="flex justify-center py-12">
          <Spinner size="lg">Loading customers...</Spinner>
        </div>
      {:else if customers.length === 0}
        <Card>
          <div class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <h3 class="mt-2 text-lg font-medium text-gray-900">No customers found</h3>
            <p class="mt-1 text-sm text-gray-500">
              {searchQuery ? 'Try adjusting your search' : 'Get started by adding your first customer'}
            </p>
            <div class="mt-6">
              {#if searchQuery}
                <Button variant="outline" on:click={() => {
                  searchQuery = '';
                  loadCustomers();
                }}>
                  Clear Search
                </Button>
              {:else}
                <Button on:click={() => showNewCustomerModal = true}>
                  Add Customer
                </Button>
              {/if}
            </div>
          </div>
        </Card>
      {:else}
        <Card>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contact
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Bookings
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Spent
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Last Visit
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="relative px-6 py-3">
                    <span class="sr-only">Actions</span>
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                {#each customers as customer}
                  <tr class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="flex items-center">
                        <Avatar
                          name={customer.user.full_name}
                          src={customer.user.avatar}
                          size="sm"
                        />
                        <div class="ml-4">
                          <div class="text-sm font-medium text-gray-900">
                            {customer.user.full_name}
                          </div>
                          {#if customer.tags && customer.tags.length > 0}
                            <div class="flex gap-1 mt-1">
                              {#each customer.tags.slice(0, 2) as tag}
                                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700">
                                  {tag}
                                </span>
                              {/each}
                              {#if customer.tags.length > 2}
                                <span class="text-xs text-gray-500">+{customer.tags.length - 2}</span>
                              {/if}
                            </div>
                          {/if}
                        </div>
                      </div>
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-900">{customer.user.email}</div>
                      {#if customer.user.phone}
                        <div class="text-sm text-gray-500">{customer.user.phone}</div>
                      {/if}
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-900">{customer.total_bookings || 0}</div>
                      {#if customer.upcoming_bookings > 0}
                        <div class="text-xs text-green-600">{customer.upcoming_bookings} upcoming</div>
                      {/if}
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      ${customer.total_spent || 0}
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {customer.last_visit 
                        ? new Date(customer.last_visit).toLocaleDateString()
                        : 'Never'}
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                        {customer.status === 'active' ? 'bg-green-100 text-green-800' : ''}
                        {customer.status === 'inactive' ? 'bg-gray-100 text-gray-800' : ''}
                        {customer.status === 'vip' ? 'bg-purple-100 text-purple-800' : ''}
                      ">
                        {customer.status || 'active'}
                      </span>
                    </td>
                    
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <div class="flex items-center justify-end space-x-2">
                        <Button
                          size="sm"
                          variant="outline"
                          on:click={() => loadCustomerDetails(customer)}
                        >
                          View
                        </Button>
                        
                        <Button
                          size="sm"
                          variant="outline"
                          on:click={() => sendMessage(customer)}
                        >
                          Message
                        </Button>
                      </div>
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </Card>
        
        <!-- Pagination -->
        {#if totalPages > 1}
          <div class="mt-6">
            <Pagination
              bind:currentPage
              {totalPages}
              on:change={loadCustomers}
            />
          </div>
        {/if}
      {/if}
    </div>
    
    <!-- Customer Details Modal -->
    <Modal bind:open={showDetailsModal} title="Customer Details" size="lg">
      {#if selectedCustomer}
        <div class="space-y-6">
          <!-- Customer Header -->
          <div class="flex items-start justify-between">
            <div class="flex items-center space-x-4">
              <Avatar
                name={selectedCustomer.user.full_name}
                src={selectedCustomer.user.avatar}
                size="lg"
              />
              <div>
                <h3 class="text-lg font-semibold text-gray-900">
                  {selectedCustomer.user.full_name}
                </h3>
                <p class="text-sm text-gray-600">{selectedCustomer.user.email}</p>
                {#if selectedCustomer.user.phone}
                  <p class="text-sm text-gray-600">{selectedCustomer.user.phone}</p>
                {/if}
              </div>
            </div>
            
            <div class="flex gap-2">
              {#each selectedCustomer.tags || [] as tag}
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                  {tag}
                </span>
              {/each}
            </div>
          </div>
          
          <!-- Stats Grid -->
          {#if selectedCustomer.stats}
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="text-center p-3 bg-gray-50 rounded-lg">
                <p class="text-2xl font-bold text-gray-900">{selectedCustomer.stats.total_bookings}</p>
                <p class="text-xs text-gray-600">Total Bookings</p>
              </div>
              <div class="text-center p-3 bg-gray-50 rounded-lg">
                <p class="text-2xl font-bold text-gray-900">${selectedCustomer.stats.total_spent}</p>
                <p class="text-xs text-gray-600">Total Spent</p>
              </div>
              <div class="text-center p-3 bg-gray-50 rounded-lg">
                <p class="text-2xl font-bold text-gray-900">{selectedCustomer.stats.average_rating || 0}</p>
                <p class="text-xs text-gray-600">Avg Rating</p>
              </div>
              <div class="text-center p-3 bg-gray-50 rounded-lg">
                <p class="text-2xl font-bold text-gray-900">{selectedCustomer.stats.no_shows || 0}</p>
                <p class="text-xs text-gray-600">No Shows</p>
              </div>
            </div>
          {/if}
          
          <!-- Recent Bookings -->
          {#if selectedCustomer.recent_bookings && selectedCustomer.recent_bookings.length > 0}
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-3">Recent Bookings</h4>
              <div class="space-y-2">
                {#each selectedCustomer.recent_bookings as booking}
                  <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p class="text-sm font-medium text-gray-900">{booking.service.name}</p>
                      <p class="text-xs text-gray-600">
                        {new Date(booking.booking_date).toLocaleDateString()} at {booking.start_time}
                      </p>
                    </div>
                    <span class="inline-flex items-center px-2 py-1 rounded text-xs font-medium
                      {booking.status === 'completed' ? 'bg-green-100 text-green-800' : ''}
                      {booking.status === 'confirmed' ? 'bg-blue-100 text-blue-800' : ''}
                      {booking.status === 'cancelled' ? 'bg-red-100 text-red-800' : ''}
                    ">
                      {booking.status}
                    </span>
                  </div>
                {/each}
              </div>
            </div>
          {/if}
          
          <!-- Notes -->
          {#if selectedCustomer.notes}
            <div>
              <h4 class="text-sm font-medium text-gray-900 mb-2">Notes</h4>
              <p class="text-sm text-gray-600">{selectedCustomer.notes}</p>
            </div>
          {/if}
        </div>
      {/if}
      
      <div slot="footer" class="flex justify-between">
        <Button
          variant="outline"
          on:click={() => handleDeleteCustomer(selectedCustomer.id)}
        >
          Delete Customer
        </Button>
        
        <div class="flex gap-3">
          <Button
            variant="outline"
            href="/bookings/new?customer={selectedCustomer.id}"
          >
            New Booking
          </Button>
          
          <Button
            href="/customers/profile?id={selectedCustomer.id}"
          >
            View Full Profile
          </Button>
        </div>
      </div>
    </Modal>
    
    <!-- New Customer Modal -->
    <Modal bind:open={showNewCustomerModal} title="Add New Customer" size="md">
      <div class="space-y-4">
        <Input
          label="Full Name"
          bind:value={newCustomer.full_name}
          required
          placeholder="John Doe"
        />
        
        <Input
          type="email"
          label="Email Address"
          bind:value={newCustomer.email}
          required
          placeholder="john@example.com"
        />
        
        <Input
          type="tel"
          label="Phone Number"
          bind:value={newCustomer.phone}
          placeholder="+1 (555) 123-4567"
        />
        
        <Input
          type="date"
          label="Date of Birth"
          bind:value={newCustomer.date_of_birth}
        />
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Address
          </label>
          <textarea
            bind:value={newCustomer.address}
            rows="2"
            class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            placeholder="123 Main St, City, State"
          ></textarea>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Tags
          </label>
          <div class="flex flex-wrap gap-2">
            {#each tagOptions as tag}
              <button
                type="button"
                class="px-3 py-1 rounded-full text-sm font-medium transition-colors
                  {newCustomer.tags.includes(tag)
                    ? 'bg-indigo-100 text-indigo-800'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
                on:click={() => toggleTag(tag)}
              >
                {tag}
              </button>
            {/each}
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Notes
          </label>
          <textarea
            bind:value={newCustomer.notes}
            rows="3"
            class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            placeholder="Any additional notes..."
          ></textarea>
        </div>
      </div>
      
      <div slot="footer" class="flex justify-end gap-3">
        <Button variant="outline" on:click={() => {
          showNewCustomerModal = false;
          resetNewCustomerForm();
        }}>
          Cancel
        </Button>
        <Button on:click={handleCreateCustomer}>
          Create Customer
        </Button>
      </div>
    </Modal>
    
    <!-- Import Modal -->
    <Modal bind:open={showImportModal} title="Import Customers" size="md">
      <div class="space-y-4">
        <p class="text-sm text-gray-600">
          Upload a CSV file with customer data. The file should include columns for:
          name, email, phone, address, and date_of_birth.
        </p>
        
        <div class="border-2 border-dashed border-gray-300 rounded-lg p-6">
          <input
            type="file"
            accept=".csv"
            on:change={handleImport}
            class="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-indigo-50 file:text-indigo-700
              hover:file:bg-indigo-100"
          />
        </div>
        
        <Button variant="outline" size="sm" href="/templates/customers-import.csv">
          Download Template
        </Button>
      </div>
      
      <div slot="footer" class="flex justify-end">
        <Button variant="outline" on:click={() => showImportModal = false}>
          Cancel
        </Button>
      </div>
    </Modal>
  </div>