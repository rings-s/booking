<!-- src/routes/bookings/new/+page.svelte -->
<script>
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { bookingAPI } from '$lib/api/bookings';
  import { businessAPI } from '$lib/api/businesses';
  import { servicesAPI } from '$lib/api/services';
  import { customerAPI } from '$lib/api/customers';
  import BookingCalendar from '$lib/components/booking/BookingCalendar.svelte';
  import TimeSlotPicker from '$lib/components/booking/TimeSlotPicker.svelte';
  import Button from '$lib/components/common/Button.svelte';
  import Card from '$lib/components/common/Card.svelte';
  import Alert from '$lib/components/common/Alert.svelte';
  import Input from '$lib/components/common/Input.svelte';
  import Select from '$lib/components/common/Select.svelte';
  import Spinner from '$lib/components/common/Spinner.svelte';
  import toast from 'svelte-french-toast';
  
  // Get URL params for pre-selection
  const businessId = $page.url.searchParams.get('business');
  const serviceId = $page.url.searchParams.get('service');
  const customerId = $page.url.searchParams.get('customer');
  
  let currentStep = 1;
  let loading = false;
  let businesses = [];
  let services = [];
  let customers = [];
  let availableSlots = [];
  let loadingSlots = false;
  
  // Booking data
  let bookingData = {
    business_id: businessId || '',
    service_id: serviceId || '',
    customer_id: customerId || '',
    booking_date: '',
    start_time: '',
    end_time: '',
    notes: '',
    send_confirmation: true,
    send_reminder: true
  };
  
  // For new customer
  let isNewCustomer = false;
  let newCustomerData = {
    full_name: '',
    email: '',
    phone: ''
  };
  
  let selectedBusiness = null;
  let selectedService = null;
  let selectedDate = null;
  let selectedTimeSlot = null;
  
  onMount(async () => {
    await loadInitialData();
    
    // If pre-selected, advance to appropriate step
    if (businessId && serviceId) {
      await loadServices();
      selectedService = services.find(s => s.id === serviceId);
      currentStep = 2;
    }
  });
  
  async function loadInitialData() {
    loading = true;
    
    const [businessesRes, customersRes] = await Promise.all([
      businessAPI.getMyBusinesses(),
      customerAPI.getAll()
    ]);
    
    if (businessesRes.data) {
      businesses = businessesRes.data;
      if (businessId) {
        bookingData.business_id = businessId;
        selectedBusiness = businesses.find(b => b.id === businessId);
        await loadServices();
      } else if (businesses.length === 1) {
        bookingData.business_id = businesses[0].id;
        selectedBusiness = businesses[0];
        await loadServices();
      }
    }
    
    if (customersRes.data) {
      customers = customersRes.data;
      if (customerId) {
        bookingData.customer_id = customerId;
      }
    }
    
    loading = false;
  }
  
  async function loadServices() {
    if (!bookingData.business_id) return;
    
    const { data } = await servicesAPI.getByBusiness(bookingData.business_id);
    if (data) {
      services = data.filter(s => s.is_active);
      if (serviceId) {
        bookingData.service_id = serviceId;
        selectedService = services.find(s => s.id === serviceId);
      }
    }
  }
  
  async function loadAvailableSlots() {
    if (!bookingData.service_id || !selectedDate) return;
    
    loadingSlots = true;
    
    const { data } = await bookingAPI.getAvailableSlots({
      service_id: bookingData.service_id,
      date: selectedDate,
      business_id: bookingData.business_id
    });
    
    if (data) {
      availableSlots = data;
    }
    
    loadingSlots = false;
  }
  
  async function handleSubmit() {
    loading = true;
    
    try {
      // Create new customer if needed
      if (isNewCustomer) {
        const { data: customerData } = await customerAPI.create(newCustomerData);
        if (customerData) {
          bookingData.customer_id = customerData.id;
        } else {
          throw new Error('Failed to create customer');
        }
      }
      
      // Prepare booking data
      const payload = {
        ...bookingData,
        booking_date: selectedDate,
        start_time: selectedTimeSlot.start_time,
        end_time: selectedTimeSlot.end_time
      };
      
      // Create booking
      const { data, error } = await bookingAPI.create(payload);
      
      if (data) {
        toast.success('Booking created successfully!');
        goto(`/bookings/${data.id}`);
      } else {
        throw new Error(error || 'Failed to create booking');
      }
    } catch (error) {
      toast.error(error.message);
      loading = false;
    }
  }
  
  // Calculate total price
  $: totalPrice = selectedService ? selectedService.price : 0;
</script>

<div class="min-h-screen bg-gray-50">
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <!-- Header -->
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Create New Booking</h1>
      <p class="mt-2 text-gray-600">Schedule an appointment in just a few steps</p>
    </div>
    
    {#if currentStep === 1}
      <!-- Step 1: Select Business & Service -->
      <Card title="Select Business & Service">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Business Selection -->
          <div>
            <label for="business" class="block text-sm font-medium text-gray-700 mb-2">
              Business
            </label>
            <Select
              id="business"
              bind:value={bookingData.business_id}
              required
              on:change={loadBusinessServices}
            >
              <option value="">Select a business</option>
              {#each businesses as business}
                <option value={business.id}>{business.name}</option>
              {/each}
            </Select>
          </div>

          <!-- Service Selection -->
          <div>
            <label for="service" class="block text-sm font-medium text-gray-700 mb-2">
              Service
            </label>
            <Select
              id="service"
              bind:value={bookingData.service_id}
              required
              disabled={!bookingData.business_id}
            >
              <option value="">Select a service</option>
              {#each services as service}
                <option value={service.id}>
                  {service.name} - ${service.price} ({service.duration_minutes}min)
                </option>
              {/each}
            </Select>
          </div>
        </div>

        {#if selectedService}
          <div class="mt-6 p-4 bg-blue-50 rounded-lg">
            <h3 class="font-medium text-blue-900 mb-2">{selectedService.name}</h3>
            {#if selectedService.description}
              <p class="text-sm text-blue-700 mb-3">{selectedService.description}</p>
            {/if}
            <div class="flex items-center justify-between text-sm text-blue-800">
              <span>Duration: {selectedService.duration_minutes} minutes</span>
              <span class="font-medium">${selectedService.price}</span>
            </div>
          </div>
        {/if}
      </Card>
    {:else if currentStep === 2}
      <!-- Step 2: Select Date & Time with Fixed Calendar -->
      <Card title="Select Date & Time">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Calendar -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-4">
              Select Date
            </label>
            <BookingCalendar
              bind:selectedDate
              businessId={bookingData.business_id}
              serviceId={bookingData.service_id}
              minDate={new Date().toISOString().split('T')[0]}
              maxDate={new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]}
              on:change={loadAvailableSlots}
            />
          </div>
          
          <!-- Time Slots -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-4">
              Available Time Slots
            </label>
            
            {#if loadingSlots}
              <div class="flex justify-center py-8">
                <Spinner>Loading available times...</Spinner>
              </div>
            {:else if selectedDate && availableSlots.length > 0}
              <TimeSlotPicker
                slots={availableSlots}
                bind:selectedSlot={selectedTimeSlot}
                serviceDuration={selectedService?.duration_minutes}
              />
            {:else if selectedDate}
              <Alert type="warning">
                No available time slots for this date. Please select another date.
              </Alert>
            {:else}
              <Alert type="info">
                Please select a date to see available time slots.
              </Alert>
            {/if}
          </div>
        </div>
        
        {#if selectedService && selectedDate && selectedTimeSlot}
          <div class="mt-6 p-4 bg-indigo-50 rounded-lg">
            <h4 class="text-sm font-medium text-indigo-900 mb-2">Booking Summary</h4>
            <dl class="space-y-1 text-sm">
              <div class="flex justify-between">
                <dt class="text-indigo-700">Service:</dt>
                <dd class="font-medium text-indigo-900">{selectedService.name}</dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-indigo-700">Date:</dt>
                <dd class="font-medium text-indigo-900">
                  {new Date(selectedDate).toLocaleDateString()}
                </dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-indigo-700">Time:</dt>
                <dd class="font-medium text-indigo-900">
                  {selectedTimeSlot.start_time} - {selectedTimeSlot.end_time}
                </dd>
              </div>
              <div class="flex justify-between">
                <dt class="text-indigo-700">Duration:</dt>
                <dd class="font-medium text-indigo-900">
                  {selectedService.duration_minutes} minutes
                </dd>
              </div>
              <div class="flex justify-between pt-2 border-t border-indigo-200">
                <dt class="text-indigo-700 font-medium">Total:</dt>
                <dd class="font-bold text-indigo-900">${totalPrice}</dd>
              </div>
            </dl>
          </div>
        {/if}
      </Card>
    {:else if currentStep === 3}
      <!-- Step 3: Customer Information -->
      <Card title="Customer Information">
        <div class="mb-6">
          <label class="flex items-center">
            <input
              type="checkbox"
              bind:checked={isNewCustomer}
              class="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
            <span class="ml-2 text-sm text-gray-700">Create new customer</span>
          </label>
        </div>

        {#if isNewCustomer}
          <!-- New Customer Form -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Input
              label="Full Name"
              bind:value={newCustomerData.full_name}
              required
              placeholder="Enter customer's full name"
            />
            <Input
              label="Email"
              type="email"
              bind:value={newCustomerData.email}
              required
              placeholder="customer@example.com"
            />
            <Input
              label="Phone"
              type="tel"
              bind:value={newCustomerData.phone}
              placeholder="+1 (555) 123-4567"
            />
            <Input
              label="Date of Birth"
              type="date"
              bind:value={newCustomerData.date_of_birth}
            />
          </div>
        {:else}
          <!-- Existing Customer Selection -->
          <div>
            <label for="customer" class="block text-sm font-medium text-gray-700 mb-2">
              Select Customer
            </label>
            <Select
              id="customer"
              bind:value={bookingData.customer_id}
              required
            >
              <option value="">Select a customer</option>
              {#each customers as customer}
                <option value={customer.id}>
                  {customer.full_name} - {customer.email}
                </option>
              {/each}
            </Select>
          </div>
        {/if}

        <!-- Notes -->
        <div class="mt-6">
          <label for="notes" class="block text-sm font-medium text-gray-700 mb-2">
            Notes (Optional)
          </label>
          <textarea
            id="notes"
            bind:value={bookingData.notes}
            rows="3"
            class="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            placeholder="Any special requests or notes for this appointment..."
          ></textarea>
        </div>

        <!-- Notification Preferences -->
        <div class="mt-6 space-y-3">
          <h3 class="text-sm font-medium text-gray-700">Notification Preferences</h3>
          <label class="flex items-center">
            <input
              type="checkbox"
              bind:checked={bookingData.send_confirmation}
              class="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
            <span class="ml-2 text-sm text-gray-700">Send confirmation email</span>
          </label>
          <label class="flex items-center">
            <input
              type="checkbox"
              bind:checked={bookingData.send_reminder}
              class="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            />
            <span class="ml-2 text-sm text-gray-700">Send reminder 24 hours before</span>
          </label>
        </div>
      </Card>
    {:else if currentStep === 4}
      <!-- Step 4: Review & Confirm -->
      <Card title="Review & Confirm Booking">
        <div class="space-y-6">
          <!-- Booking Summary -->
          <div class="bg-gray-50 rounded-lg p-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Booking Summary</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <dt class="text-sm font-medium text-gray-500">Business</dt>
                <dd class="mt-1 text-sm text-gray-900">{selectedBusiness?.name}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Service</dt>
                <dd class="mt-1 text-sm text-gray-900">{selectedService?.name}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Date</dt>
                <dd class="mt-1 text-sm text-gray-900">{selectedDate}</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Time</dt>
                <dd class="mt-1 text-sm text-gray-900">
                  {selectedTimeSlot?.start_time} - {selectedTimeSlot?.end_time}
                </dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Duration</dt>
                <dd class="mt-1 text-sm text-gray-900">{selectedService?.duration_minutes} minutes</dd>
              </div>
              <div>
                <dt class="text-sm font-medium text-gray-500">Price</dt>
                <dd class="mt-1 text-lg font-medium text-gray-900">${totalPrice}</dd>
              </div>
            </div>
            {#if bookingData.notes}
              <div class="mt-4">
                <dt class="text-sm font-medium text-gray-500">Notes</dt>
                <dd class="mt-1 text-sm text-gray-900">{bookingData.notes}</dd>
              </div>
            {/if}
          </div>

          <!-- Customer Information -->
          <div class="bg-blue-50 rounded-lg p-6">
            <h3 class="text-lg font-medium text-blue-900 mb-4">Customer Information</h3>
            {#if isNewCustomer}
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <dt class="font-medium text-blue-700">Name</dt>
                  <dd class="text-blue-900">{newCustomerData.full_name}</dd>
                </div>
                <div>
                  <dt class="font-medium text-blue-700">Email</dt>
                  <dd class="text-blue-900">{newCustomerData.email}</dd>
                </div>
                {#if newCustomerData.phone}
                  <div>
                    <dt class="font-medium text-blue-700">Phone</dt>
                    <dd class="text-blue-900">{newCustomerData.phone}</dd>
                  </div>
                {/if}
              </div>
            {:else}
              <div class="text-sm">
                <dt class="font-medium text-blue-700">Customer</dt>
                <dd class="text-blue-900">{selectedCustomer?.full_name} - {selectedCustomer?.email}</dd>
              </div>
            {/if}
          </div>

          <!-- Confirmation -->
          <Alert type="info">
            <div class="flex">
              <svg class="flex-shrink-0 w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-blue-800">Please Review</h3>
                <div class="mt-2 text-sm text-blue-700">
                  <p>Please review all the details above carefully before confirming your booking.</p>
                  {#if bookingData.send_confirmation}
                    <p class="mt-1">A confirmation email will be sent to the customer.</p>
                  {/if}
                  {#if bookingData.send_reminder}
                    <p class="mt-1">A reminder will be sent 24 hours before the appointment.</p>
                  {/if}
                </div>
              </div>
            </div>
          </Alert>
        </div>
      </Card>
    {/if}
    
    <!-- Navigation -->
    <div class="flex justify-between mt-8">
      {#if currentStep > 1}
        <Button variant="outline" on:click={() => currentStep--}>
          Back
        </Button>
      {:else}
        <div></div>
      {/if}
      
      <div class="flex gap-3">
        <Button variant="outline" href="/bookings">
          Cancel
        </Button>
        
        {#if currentStep === 4}
          <Button on:click={handleSubmit} {loading}>
            Confirm Booking
          </Button>
        {:else}
          <Button on:click={() => currentStep++} disabled={
            (currentStep === 2 && (!selectedDate || !selectedTimeSlot))
          }>
            Next Step
          </Button>
        {/if}
      </div>
    </div>
  </div>
</div>