<!-- src/lib/components/booking/BookingCard.svelte -->
<script>
  import { goto } from '$app/navigation';
  import { formatDate, formatTime, formatCurrency, formatRelativeTime } from '$lib/utils/formatters';
  import Card from '../common/Card.svelte';
  import BookingStatus from './BookingStatus.svelte';
  import Button from '../common/Button.svelte';
  import Avatar from '../common/Avatar.svelte';
  import Modal from '../common/Modal.svelte';
  import { bookingStore } from '$lib/stores/booking';
  import toast from 'svelte-french-toast';
  
  let {
    booking,
    showActions = true,
    customerView = false,
    compact = false,
    oncancel = () => {},
    onconfirm = () => {},
    onupdate = () => {},
    ...restProps
  } = $props();
  
  let showCancelModal = $state(false);
  let cancelReason = $state('');
  let processing = $state(false);
  
  function handleView() {
    goto(`/bookings/${booking.id}`);
  }
  
  function handleEdit() {
    goto(`/bookings/${booking.id}/edit`);
  }
  
  async function handleCancel() {
    if (!cancelReason.trim()) {
      toast.error('Please provide a cancellation reason');
      return;
    }
    
    processing = true;
    const { error } = await bookingStore.cancelBooking(booking.id, cancelReason);
    
    if (!error) {
      showCancelModal = false;
      oncancel(booking);
    }
    processing = false;
  }
  
  async function handleConfirm() {
    processing = true;
    const { error } = await bookingStore.confirmBooking(booking.id);
    
    if (!error) {
      onconfirm(booking);
    }
    processing = false;
  }
  
  async function handleComplete() {
    processing = true;
    const { error } = await bookingStore.completeBooking(booking.id);
    
    if (!error) {
      onupdate(booking);
    }
    processing = false;
  }
  
  async function handleNoShow() {
    processing = true;
    const { error } = await bookingStore.markAsNoShow(booking.id);
    
    if (!error) {
      onupdate(booking);
    }
    processing = false;
  }
  
  function handleReview() {
    goto(`/reviews/new?booking=${booking.id}`);
  }
  
  function handleReschedule() {
    goto(`/bookings/${booking.id}/reschedule`);
  }
  
  function handlePayment() {
    goto(`/bookings/${booking.id}/payment`);
  }
  
  // Determine if booking is upcoming, past, or today
  let isToday = $derived(new Date(booking.booking_date).toDateString() === new Date().toDateString());
  let isPast = $derived(new Date(booking.booking_date) < new Date() && !isToday);
  let isUpcoming = $derived(new Date(booking.booking_date) > new Date());
  
  // Determine available actions based on status and time
  let canCancel = $derived(['pending', 'confirmed'].includes(booking.status) && !isPast);
  let canConfirm = $derived(booking.status === 'pending' && !customerView && !isPast);
  let canComplete = $derived(booking.status === 'confirmed' && !customerView && (isPast || isToday));
  let canMarkNoShow = $derived(booking.status === 'confirmed' && !customerView && isPast);
  let canReschedule = $derived(['pending', 'confirmed'].includes(booking.status) && !isPast);
  let canReview = $derived(booking.status === 'completed' && customerView && !booking.review);
  let canPay = $derived(!booking.is_paid && ['pending', 'confirmed'].includes(booking.status));
</script>

<Card padding={compact ? 'sm' : 'md'}>
  <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
    <!-- Left Section: Main Info -->
    <div class="flex-1">
      <!-- Status and ID -->
      <div class="flex items-center gap-3 mb-3">
        <BookingStatus status={booking.status} size="sm" />
        <span class="text-xs text-gray-500">ID: #{booking.id.slice(0, 8).toUpperCase()}</span>
        {#if isToday}
          <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
            Today
          </span>
        {/if}
      </div>
      
      <!-- Service Name -->
      <h3 class="text-lg font-semibold text-gray-900 mb-2">
        {booking.service.name}
      </h3>
      
      <!-- Business/Customer Info -->
      <div class="space-y-2">
        {#if customerView}
          <!-- Show business info for customers -->
          <div class="flex items-center gap-3">
            {#if booking.business.logo}
              <img
                src={booking.business.logo}
                alt={booking.business.name}
                class="w-10 h-10 rounded-full object-cover"
              />
            {:else}
              <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center">
                <svg class="w-6 h-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
            {/if}
            <div>
              <p class="text-sm font-medium text-gray-900">{booking.business.name}</p>
              <p class="text-xs text-gray-500">{booking.business.category}</p>
            </div>
          </div>
        {:else}
          <!-- Show customer info for business owners -->
          <div class="flex items-center gap-3">
            <Avatar
              name={booking.customer.user.full_name}
              size="sm"
            />
            <div>
              <p class="text-sm font-medium text-gray-900">{booking.customer.user.full_name}</p>
              <p class="text-xs text-gray-500">{booking.customer.user.email}</p>
              {#if booking.customer.phone}
                <p class="text-xs text-gray-500">{booking.customer.phone}</p>
              {/if}
            </div>
          </div>
        {/if}
        
        <!-- Date and Time -->
        <div class="flex items-center gap-4 text-sm">
          <div class="flex items-center text-gray-600">
            <svg class="w-4 h-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            {formatDate(booking.booking_date)}
          </div>
          <div class="flex items-center text-gray-600">
            <svg class="w-4 h-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {formatTime(booking.start_time)} - {formatTime(booking.end_time)}
          </div>
        </div>
        
        <!-- Location if available -->
        {#if !customerView && booking.business.address}
          <div class="flex items-start text-sm text-gray-600">
            <svg class="w-4 h-4 mr-1.5 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>{booking.business.address}, {booking.business.city}</span>
          </div>
        {/if}
        
        <!-- Notes -->
        {#if booking.notes && !compact}
          <div class="mt-2 p-3 bg-gray-50 rounded-md">
            <p class="text-xs font-medium text-gray-700 mb-1">Notes:</p>
            <p class="text-sm text-gray-600">{booking.notes}</p>
          </div>
        {/if}
      </div>
    </div>
    
    <!-- Right Section: Price and Payment Status -->
    <div class="flex flex-col items-end gap-2">
      <div class="text-right">
        <p class="text-2xl font-bold text-gray-900">
          {formatCurrency(booking.total_price)}
        </p>
        <p class="text-xs text-gray-500">
          Duration: {booking.service.duration_minutes} min
        </p>
      </div>
      
      <!-- Payment Status -->
      <div class="flex items-center gap-2">
        {#if booking.is_paid}
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            Paid
          </span>
        {:else}
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
            <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
            Unpaid
          </span>
        {/if}
        
        {#if booking.payment_method}
          <span class="text-xs text-gray-500">
            via {booking.payment_method}
          </span>
        {/if}
      </div>
      
      <!-- Created time -->
      <p class="text-xs text-gray-400">
        Booked {formatRelativeTime(booking.created_at)}
      </p>
    </div>
  </div>
  
  <!-- Actions -->
  {#if showActions && !compact}
    <div class="mt-4 pt-4 border-t border-gray-200">
      <div class="flex flex-wrap gap-2">
        <Button size="sm" variant="outline" on:click={handleView}>
          <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          View
        </Button>
        
        {#if canReschedule}
          <Button size="sm" variant="outline" on:click={handleReschedule}>
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Reschedule
          </Button>
        {/if}
        
        {#if canConfirm}
          <Button size="sm" variant="success" on:click={handleConfirm} loading={processing}>
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Confirm
          </Button>
        {/if}
        
        {#if canComplete}
          <Button size="sm" variant="success" on:click={handleComplete} loading={processing}>
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Complete
          </Button>
        {/if}
        
        {#if canMarkNoShow}
          <Button size="sm" variant="outline" on:click={handleNoShow} loading={processing}>
            No Show
          </Button>
        {/if}
        
        {#if canCancel}
          <Button size="sm" variant="danger" on:click={() => showCancelModal = true}>
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            Cancel
          </Button>
        {/if}
        
        {#if canPay}
          <Button size="sm" variant="primary" on:click={handlePayment}>
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
            </svg>
            Pay Now
          </Button>
        {/if}
        
        {#if canReview}
          <Button size="sm" variant="outline" on:click={handleReview}>
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
            Leave Review
          </Button>
        {/if}
      </div>
    </div>
  {/if}
</Card>

<!-- Cancel Modal -->
<Modal bind:open={showCancelModal} title="Cancel Booking" size="md" footer={cancelFooter}>
  <div class="space-y-4">
    <Alert type="warning">
      Are you sure you want to cancel this booking? This action cannot be undone.
    </Alert>
    
    <div>
      <label for="cancel-reason" class="block text-sm font-medium text-gray-700 mb-1">
        Cancellation Reason <span class="text-red-500">*</span>
      </label>
      <textarea
        id="cancel-reason"
        bind:value={cancelReason}
        rows="3"
        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        placeholder="Please provide a reason for cancellation..."
      ></textarea>
    </div>
    
    <div class="bg-gray-50 rounded-lg p-4">
      <h4 class="text-sm font-medium text-gray-900 mb-2">Booking Details:</h4>
      <dl class="text-sm space-y-1">
        <div class="flex justify-between">
          <dt class="text-gray-500">Service:</dt>
          <dd class="text-gray-900">{booking.service.name}</dd>
        </div>
        <div class="flex justify-between">
          <dt class="text-gray-500">Date:</dt>
          <dd class="text-gray-900">{formatDate(booking.booking_date)}</dd>
        </div>
        <div class="flex justify-between">
          <dt class="text-gray-500">Time:</dt>
          <dd class="text-gray-900">{formatTime(booking.start_time)}</dd>
        </div>
      </dl>
    </div>
  </div>
</Modal>

{#snippet cancelFooter()}
  <div class="flex justify-end gap-3">
    <Button variant="outline" on:click={() => showCancelModal = false}>
      Keep Booking
    </Button>
    <Button variant="danger" on:click={handleCancel} loading={processing}>
      Cancel Booking
    </Button>
  </div>
{/snippet}