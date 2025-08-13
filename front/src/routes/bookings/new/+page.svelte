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
    
    {#if currentStep === 2}
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