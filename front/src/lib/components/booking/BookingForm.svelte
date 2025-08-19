<!-- src/lib/components/booking/BookingForm.svelte -->
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { bookingStore } from '$lib/stores/booking';
    import { businessAPI } from '$lib/api/businesses';
    import Input from '../common/Input.svelte';
    import Select from '../common/Select.svelte';
    import Button from '../common/Button.svelte';
    import Alert from '../common/Alert.svelte';
    import Card from '../common/Card.svelte';
    import BookingCalendar from './BookingCalendar.svelte';
    import TimeSlotPicker from './TimeSlotPicker.svelte';
    import { formatCurrency, formatDuration, formatDate, formatTime } from '$lib/utils/formatters';
    import { validateForm, bookingSchema } from '$lib/utils/validators';
    import toast from 'svelte-french-toast';
    
    let {
        business,
        service = null,
        booking = null,
        customerInfo = null,
        onsubmit = () => {},
        oncancel = () => {},
        ...restProps
    } = $props();
    
    let currentStep = $state(1);
    let loading = $state(false);
    let loadingSlots = $state(false);
    let loadingDates = false;
    let errors = $state({});
    let termsAccepted = $state(false);
    
    let formData = {
      business_id: business.id,
      service_id: booking?.service?.id || service?.id || '',
      booking_date: booking?.booking_date || '',
      start_time: booking?.start_time || '',
      end_time: booking?.end_time || '',
      notes: booking?.notes || '',
      customer_name: customerInfo?.name || '',
      customer_email: customerInfo?.email || '',
      customer_phone: customerInfo?.phone || ''
    };
    
    let selectedDate = $state(null);
    let selectedSlot = $state(null);
    let availableSlots = $state([]);
    let availableDates = $state([]);
    let selectedService = $state(service || booking?.service || null);
    let services = $state([]);
    let maxDate = new Date();
    maxDate.setDate(maxDate.getDate() + 90); // Allow booking up to 90 days in advance
    
    onMount(async () => {
      // Load services if not provided
      if (!selectedService && business.id) {
        const { data } = await businessAPI.get(business.slug);
        if (data) {
          services = data.services?.filter(s => s.is_active) || [];
          if (services.length > 0 && !formData.service_id) {
            selectedService = services[0];
            formData.service_id = selectedService.id;
            await loadAvailableDates();
          }
        }
      } else if (selectedService) {
        services = [selectedService];
        await loadAvailableDates();
      }
    });

    async function loadAvailableDates() {
      if (!selectedService) return;
      
      loadingDates = true;
      try {
        const { data, error } = await bookingStore.loadAvailableDates(
          business.slug,
          selectedService.id,
          90
        );
        
        if (data) {
          availableDates = data.available_dates || [];
        } else if (error) {
          toast.error(error);
          availableDates = [];
        }
      } catch (err) {
        toast.error('Failed to load available dates');
        availableDates = [];
      } finally {
        loadingDates = false;
      }
    }
    
    async function handleDateSelect(event) {
      selectedDate = event.detail;
      formData.booking_date = formatDate(selectedDate, 'yyyy-MM-dd');
      
      if (selectedService) {
        loadingSlots = true;
        const { data } = await bookingStore.loadAvailableSlots(
          business.slug,
          selectedService.id,
          formData.booking_date
        );
        
        if (data) {
          availableSlots = data.slots || [];
          if (availableSlots.length === 0) {
            toast.error('No available slots for this date');
          } else {
            currentStep = 2;
          }
        }
        loadingSlots = false;
      }
    }
    
    function handleSlotSelect(event) {
      selectedSlot = event.detail;
      formData.start_time = selectedSlot.start_time;
      formData.end_time = selectedSlot.end_time;
      currentStep = 3;
    }
    
    async function handleServiceChange() {
      selectedService = services.find(s => s.id === formData.service_id);
      
      // Reset date and time selection when service changes
      selectedDate = null;
      selectedSlot = null;
      formData.booking_date = '';
      formData.start_time = '';
      formData.end_time = '';
      availableSlots = [];
      availableDates = [];
      
      // Load available dates for the new service
      if (selectedService) {
        await loadAvailableDates();
      }
    }
    
    async function handleSubmit() {
      // Validate required fields
      if (!termsAccepted) {
        toast.error('Please accept the terms and conditions');
        return;
      }
      
      const validation = await validateForm(bookingSchema, formData);
      
      if (!validation.isValid) {
        errors = validation.errors;
        toast.error('Please check all required fields');
        return;
      }
      
      loading = true;
      errors = {};
      
      const bookingData = {
        business_id: business.id,
        service_id: formData.service_id,
        booking_date: formData.booking_date,
        start_time: formData.start_time,
        end_time: formData.end_time,
        notes: formData.notes,
        total_price: selectedService.price
      };
      
      const { data, error } = booking 
        ? await bookingStore.updateBooking(booking.id, bookingData)
        : await bookingStore.createBooking(bookingData);
      
      if (error) {
        toast.error(error);
      } else {
        toast.success(booking ? 'Booking updated successfully!' : 'Booking created successfully!');
        onsubmit(data);
        
        // Redirect to booking details
        goto(`/bookings/${data.id}`);
      }
      
      loading = false;
    }
    
    function previousStep() {
      currentStep = Math.max(1, currentStep - 1);
    }
    
    function goToStep(step) {
      if (step === 1) {
        currentStep = 1;
      } else if (step === 2 && selectedService && selectedDate) {
        currentStep = 2;
      } else if (step === 3 && selectedService && selectedDate && selectedSlot) {
        currentStep = 3;
      }
    }
    
    // Calculate total with any additional fees
    let subtotal = $derived(selectedService?.price || 0);
    let serviceFee = $derived(subtotal * 0.05); // 5% service fee
    let total = $derived(subtotal + serviceFee);
  </script>
  
  <div class="max-w-4xl mx-auto">
    <!-- Progress Steps -->
    <div class="mb-8">
      <nav aria-label="Progress">
        <ol class="flex items-center">
          {#each [
            { num: 1, name: 'Select Service & Date' },
            { num: 2, name: 'Choose Time' },
            { num: 3, name: 'Confirm Booking' }
          ] as step}
            <li class="flex items-center {step.num < 3 ? 'flex-1' : ''}">
              <button
                type="button"
                class="group"
                on:click={() => goToStep(step.num)}
                disabled={step.num > currentStep}
              >
                <span class="flex items-center">
                  <span class="
                    w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium
                    {currentStep >= step.num 
                      ? 'bg-indigo-600 text-white' 
                      : 'bg-gray-200 text-gray-600'}
                  ">
                    {#if currentStep > step.num}
                      <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                    {:else}
                      {step.num}
                    {/if}
                  </span>
                  <span class="ml-2 text-sm font-medium {currentStep >= step.num ? 'text-gray-900' : 'text-gray-500'}">
                    {step.name}
                  </span>
                </span>
              </button>
              
              {#if step.num < 3}
                <div class="flex-1 h-0.5 mx-4 {currentStep > step.num ? 'bg-indigo-600' : 'bg-gray-200'}"></div>
              {/if}
            </li>
          {/each}
        </ol>
      </nav>
    </div>
    
    <form on:submit|preventDefault={handleSubmit}>
      {#if currentStep === 1}
        <!-- Step 1: Select Service and Date -->
        <div class="space-y-6">
          <Card title="Select a Service">
            {#if services.length > 0}
              <div class="space-y-3">
                {#each services as serviceOption}
                  <label class="
                    relative flex items-start p-4 border-2 rounded-lg cursor-pointer transition-colors
                    {formData.service_id === serviceOption.id 
                      ? 'border-indigo-600 bg-indigo-50' 
                      : 'border-gray-200 hover:border-gray-300'}
                  ">
                    <input
                      type="radio"
                      name="service"
                      value={serviceOption.id}
                      bind:group={formData.service_id}
                      on:change={handleServiceChange}
                      class="h-4 w-4 mt-1 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                    />
                    <div class="ml-3 flex-1">
                      <div class="flex items-start justify-between">
                        <div>
                          <span class="block text-base font-medium text-gray-900">
                            {serviceOption.name}
                          </span>
                          <span class="block text-sm text-gray-500 mt-1">
                            {serviceOption.description}
                          </span>
                        </div>
                        <div class="ml-4 text-right">
                          <span class="block text-lg font-semibold text-gray-900">
                            {formatCurrency(serviceOption.price)}
                          </span>
                          <span class="block text-sm text-gray-500">
                            {formatDuration(serviceOption.duration_minutes)}
                          </span>
                        </div>
                      </div>
                      
                      {#if serviceOption.max_bookings_per_slot > 1}
                        <div class="mt-2">
                          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            Group booking available (max {serviceOption.max_bookings_per_slot})
                          </span>
                        </div>
                      {/if}
                    </div>
                  </label>
                {/each}
              </div>
            {:else}
              <Alert type="warning" message="No services available for booking" />
            {/if}
          </Card>
          
          {#if selectedService}
            <Card title="Select a Date">
              <BookingCalendar
                businessHours={business.hours || business.business_hours || []}
                {availableDates}
                loading={loadingDates}
                on:select={handleDateSelect}
                bind:selectedDate
                minDate={new Date()}
                {maxDate}
              />
            </Card>
          {/if}
        </div>
      {/if}
      
      {#if currentStep === 2}
        <!-- Step 2: Select Time -->
        <div class="space-y-6">
          <Card>
            <div class="bg-indigo-50 rounded-lg p-4 mb-6">
              <dl class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <dt class="font-medium text-gray-600">Service:</dt>
                  <dd class="mt-1 font-semibold text-gray-900">{selectedService.name}</dd>
                </div>
                <div>
                  <dt class="font-medium text-gray-600">Date:</dt>
                  <dd class="mt-1 font-semibold text-gray-900">{formatDate(selectedDate)}</dd>
                </div>
                <div>
                  <dt class="font-medium text-gray-600">Duration:</dt>
                  <dd class="mt-1 font-semibold text-gray-900">{formatDuration(selectedService.duration_minutes)}</dd>
                </div>
                <div>
                  <dt class="font-medium text-gray-600">Price:</dt>
                  <dd class="mt-1 font-semibold text-gray-900">{formatCurrency(selectedService.price)}</dd>
                </div>
              </dl>
            </div>
            
            <TimeSlotPicker
              slots={availableSlots}
              bind:selectedSlot
              on:select={handleSlotSelect}
              loading={loadingSlots}
            />
          </Card>
          
          <div class="flex justify-between">
            <Button type="button" variant="outline" on:click={previousStep}>
              Back
            </Button>
          </div>
        </div>
      {/if}
      
      {#if currentStep === 3}
        <!-- Step 3: Confirm and Add Notes -->
        <div class="space-y-6">
          <Card title="Booking Summary">
            <div class="bg-gray-50 rounded-lg p-6">
              <dl class="space-y-4">
                <div class="flex justify-between">
                  <dt class="text-sm text-gray-600">Business:</dt>
                  <dd class="text-sm font-medium text-gray-900">{business.name}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-sm text-gray-600">Service:</dt>
                  <dd class="text-sm font-medium text-gray-900">{selectedService.name}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-sm text-gray-600">Date:</dt>
                  <dd class="text-sm font-medium text-gray-900">{formatDate(selectedDate, 'EEEE, MMMM d, yyyy')}</dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-sm text-gray-600">Time:</dt>
                  <dd class="text-sm font-medium text-gray-900">
                    {formatTime(selectedSlot.start_time)} - {formatTime(selectedSlot.end_time)}
                  </dd>
                </div>
                <div class="flex justify-between">
                  <dt class="text-sm text-gray-600">Duration:</dt>
                  <dd class="text-sm font-medium text-gray-900">
                    {formatDuration(selectedService.duration_minutes)}
                  </dd>
                </div>
                
                <div class="pt-4 border-t border-gray-200 space-y-2">
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-600">Service Price:</dt>
                    <dd class="text-sm text-gray-900">{formatCurrency(subtotal)}</dd>
                  </div>
                  <div class="flex justify-between">
                    <dt class="text-sm text-gray-600">Service Fee:</dt>
                    <dd class="text-sm text-gray-900">{formatCurrency(serviceFee)}</dd>
                  </div>
                  <div class="flex justify-between pt-2 border-t">
                    <dt class="text-base font-medium text-gray-900">Total:</dt>
                    <dd class="text-base font-medium text-indigo-600">
                      {formatCurrency(total)}
                    </dd>
                  </div>
                </div>
              </dl>
            </div>
          </Card>
          
          <Card title="Additional Information">
            <div class="space-y-4">
              <div>
                <label for="notes" class="block text-sm font-medium text-gray-700 mb-1">
                  Special Requests or Notes (optional)
                </label>
                <textarea
                  id="notes"
                  bind:value={formData.notes}
                  rows="4"
                  class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  placeholder="Any allergies, preferences, or special requests..."
                ></textarea>
                <p class="mt-1 text-xs text-gray-500">
                  {formData.notes.length}/500 characters
                </p>
              </div>
            </div>
          </Card>
          
          <Card title="Cancellation Policy">
            <div class="prose prose-sm text-gray-600">
              <ul>
                <li>Free cancellation up to 24 hours before your appointment</li>
                <li>50% charge for cancellations within 24 hours</li>
                <li>No refund for no-shows</li>
              </ul>
            </div>
            
            <div class="mt-4">
              <label class="flex items-start">
                <input
                  type="checkbox"
                  bind:checked={termsAccepted}
                  class="h-4 w-4 mt-1 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <span class="ml-2 text-sm text-gray-700">
                  I agree to the cancellation policy and 
                  <a href="/terms" class="text-indigo-600 hover:text-indigo-500">terms of service</a>
                </span>
              </label>
            </div>
          </Card>
          
          <div class="flex justify-between">
            <Button type="button" variant="outline" on:click={previousStep}>
              Back
            </Button>
            <Button type="submit" loading={loading} disabled={!termsAccepted}>
              {booking ? 'Update' : 'Confirm'} Booking
            </Button>
          </div>
        </div>
      {/if}
    </form>
  </div>