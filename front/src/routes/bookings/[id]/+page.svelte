<!-- src/routes/bookings/[id]/+page.svelte -->
<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { bookingAPI } from '$lib/api/bookings';
    import { notificationAPI } from '$lib/api/notifications';
    import BookingStatus from '$lib/components/booking/BookingStatus.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Alert from '$lib/components/common/Alert.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import toast from 'svelte-french-toast';
    import QRCode from 'qrcode';
    
    const bookingId = $page.params.id;
    
    let booking = null;
    let loading = true;
    let updating = false;
    let showCancelModal = false;
    let showRescheduleModal = false;
    let showPaymentModal = false;
    let showNotesModal = false;
    let additionalNotes = '';
    let qrCodeUrl = '';
    
    // Reschedule data
    let newDate = '';
    let newTime = '';
    let availableSlots = [];
    
    onMount(async () => {
      await loadBooking();
      await generateQRCode();
    });
    
    async function loadBooking() {
      loading = true;
      const { data, error } = await bookingAPI.getById(bookingId);
      
      if (data) {
        booking = data;
      } else {
        toast.error('Booking not found');
        goto('/bookings');
      }
      
      loading = false;
    }
    
    async function generateQRCode() {
      const bookingUrl = `${window.location.origin}/bookings/${bookingId}`;
      qrCodeUrl = await QRCode.toDataURL(bookingUrl);
    }
    
    async function handleStatusUpdate(newStatus) {
      updating = true;
      const { data, error } = await bookingAPI.updateStatus(bookingId, newStatus);
      
      if (data) {
        booking = data;
        toast.success(`Booking ${newStatus}`);
      } else {
        toast.error('Failed to update booking status');
      }
      
      updating = false;
    }
    
    async function handleCancel() {
      updating = true;
      const { data, error } = await bookingAPI.cancel(bookingId);
      
      if (data) {
        booking = data;
        showCancelModal = false;
        toast.success('Booking cancelled successfully');
      } else {
        toast.error('Failed to cancel booking');
      }
      
      updating = false;
    }
    
    async function handleReschedule() {
      if (!newDate || !newTime) {
        toast.error('Please select new date and time');
        return;
      }
      
      updating = true;
      const { data, error } = await bookingAPI.reschedule(bookingId, {
        booking_date: newDate,
        start_time: newTime
      });
      
      if (data) {
        booking = data;
        showRescheduleModal = false;
        toast.success('Booking rescheduled successfully');
      } else {
        toast.error('Failed to reschedule booking');
      }
      
      updating = false;
    }
    
    async function sendReminder() {
      const { data, error } = await notificationAPI.sendBookingReminder(bookingId);
      
      if (data) {
        toast.success('Reminder sent successfully');
      } else {
        toast.error('Failed to send reminder');
      }
    }
    
    async function handleAddNotes() {
      if (!additionalNotes.trim()) {
        toast.error('Please enter notes');
        return;
      }
      
      updating = true;
      const { data, error } = await bookingAPI.update(bookingId, {
        notes: (booking.notes ? booking.notes + '\n\n' : '') + additionalNotes
      });
      
      if (data) {
        booking = data;
        additionalNotes = '';
        showNotesModal = false;
        toast.success('Notes added successfully');
      }
      
      updating = false;
    }
    
    function printBooking() {
      window.print();
    }
    
    function downloadQRCode() {
      const link = document.createElement('a');
      link.download = `booking-${bookingId}.png`;
      link.href = qrCodeUrl;
      link.click();
    }
    
    // Check if booking can be modified
    $: canModify = booking && 
      ['pending', 'confirmed'].includes(booking.status) &&
      new Date(booking.booking_date) > new Date();
    
    $: isPast = booking && new Date(booking.booking_date) < new Date();
  </script>
  
  {#if loading}
    <div class="min-h-screen flex items-center justify-center">
      <Spinner size="lg">Loading booking...</Spinner>
    </div>
  {:else if booking}
    <div class="min-h-screen bg-gray-50">
      <!-- Header -->
      <div class="bg-white shadow-sm border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="py-6 flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <Button variant="outline" href="/bookings">
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Bookings
              </Button>
              
              <div>
                <h1 class="text-2xl font-bold text-gray-900">Booking Details</h1>
                <p class="text-sm text-gray-600">ID: {booking.id.slice(0, 8)}</p>
              </div>
            </div>
            
            <div class="flex items-center space-x-3">
              <Button variant="outline" on:click={printBooking}>
                <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                </svg>
                Print
              </Button>
              
              <BookingStatus status={booking.status} size="lg" />
            </div>
          </div>
        </div>
      </div>
      
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Main Content -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Service Information -->
            <Card title="Service Information">
              <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <dt class="text-sm font-medium text-gray-500">Service</dt>
                  <dd class="mt-1 text-sm text-gray-900">{booking.service.name}</dd>
                </div>
                
                <div>
                  <dt class="text-sm font-medium text-gray-500">Business</dt>
                  <dd class="mt-1 text-sm text-gray-900">{booking.business.name}</dd>
                </div>
                
                <div>
                  <dt class="text-sm font-medium text-gray-500">Duration</dt>
                  <dd class="mt-1 text-sm text-gray-900">{booking.service.duration_minutes} minutes</dd>
                </div>
                
                <div>
                  <dt class="text-sm font-medium text-gray-500">Price</dt>
                  <dd class="mt-1 text-sm font-semibold text-gray-900">${booking.total_price}</dd>
                </div>
              </dl>
              
              {#if booking.service.description}
                <div class="mt-4 pt-4 border-t border-gray-200">
                  <dt class="text-sm font-medium text-gray-500">Description</dt>
                  <dd class="mt-1 text-sm text-gray-900">{booking.service.description}</dd>
                </div>
              {/if}
            </Card>
            
            <!-- Date & Time -->
            <Card title="Date & Time">
              <div class="space-y-4">
                <div class="flex items-center justify-between p-4 bg-indigo-50 rounded-lg">
                  <div class="flex items-center space-x-4">
                    <div class="p-3 bg-indigo-100 rounded-lg">
                      <svg class="w-6 h-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <div>
                      <p class="text-sm text-indigo-600">Date</p>
                      <p class="text-lg font-semibold text-gray-900">
                        {new Date(booking.booking_date).toLocaleDateString('en-US', {
                          weekday: 'long',
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric'
                        })}
                      </p>
                    </div>
                  </div>
                  
                  <div class="flex items-center space-x-4">
                    <div class="p-3 bg-indigo-100 rounded-lg">
                      <svg class="w-6 h-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div>
                      <p class="text-sm text-indigo-600">Time</p>
                      <p class="text-lg font-semibold text-gray-900">
                        {booking.start_time} - {booking.end_time}
                      </p>
                    </div>
                  </div>
                </div>
                
                {#if canModify}
                  <Button
                    variant="outline"
                    fullWidth
                    on:click={() => showRescheduleModal = true}
                  >
                    <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Reschedule
                  </Button>
                {/if}
              </div>
            </Card>
            
            <!-- Customer Information -->
            <Card title="Customer Information">
              <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <dt class="text-sm font-medium text-gray-500">Name</dt>
                  <dd class="mt-1 text-sm text-gray-900">{booking.customer.user.full_name}</dd>
                </div>
                
                <div>
                  <dt class="text-sm font-medium text-gray-500">Email</dt>
                  <dd class="mt-1 text-sm text-gray-900">
                    <a href="mailto:{booking.customer.user.email}" class="text-indigo-600 hover:text-indigo-500">
                      {booking.customer.user.email}
                    </a>
                  </dd>
                </div>
                
                {#if booking.customer.user.phone}
                  <div>
                    <dt class="text-sm font-medium text-gray-500">Phone</dt>
                    <dd class="mt-1 text-sm text-gray-900">
                      <a href="tel:{booking.customer.user.phone}" class="text-indigo-600 hover:text-indigo-500">
                        {booking.customer.user.phone}
                      </a>
                    </dd>
                  </div>
                {/if}
                
                <div>
                  <dt class="text-sm font-medium text-gray-500">Total Bookings</dt>
                  <dd class="mt-1 text-sm text-gray-900">{booking.customer.total_bookings || 1}</dd>
                </div>
              </dl>
            </Card>
            
            <!-- Notes -->
            <Card>
              <div slot="header" class="flex items-center justify-between">
                <h3 class="text-lg font-semibold text-gray-900">Notes</h3>
                <Button size="sm" variant="outline" on:click={() => showNotesModal = true}>
                  Add Note
                </Button>
              </div>
              
              {#if booking.notes}
                <div class="whitespace-pre-wrap text-sm text-gray-900">{booking.notes}</div>
              {:else}
                <p class="text-sm text-gray-500">No notes added yet.</p>
              {/if}
            </Card>
          </div>
          
          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Actions -->
            <Card title="Actions">
              <div class="space-y-3">
                {#if booking.status === 'pending'}
                  <Button
                    fullWidth
                    on:click={() => handleStatusUpdate('confirmed')}
                    loading={updating}
                  >
                    Confirm Booking
                  </Button>
                {:else if booking.status === 'confirmed' && !isPast}
                  <Button
                    fullWidth
                    variant="outline"
                    on:click={() => handleStatusUpdate('completed')}
                    loading={updating}
                  >
                    Mark as Completed
                  </Button>
                {/if}
                
                {#if canModify}
                  <Button
                    fullWidth
                    variant="outline"
                    on:click={sendReminder}
                  >
                    Send Reminder
                  </Button>
                  
                  <Button
                    fullWidth
                    variant="outline"
                    on:click={() => showCancelModal = true}
                  >
                    Cancel Booking
                  </Button>
                {/if}
                
                {#if booking.status === 'completed' && !booking.review}
                  <Button
                    fullWidth
                    variant="outline"
                    href="/reviews/new?booking={bookingId}"
                  >
                    Request Review
                  </Button>
                {/if}
              </div>
            </Card>
            
            <!-- QR Code -->
            <Card title="QR Code">
              <div class="text-center">
                <img src={qrCodeUrl} alt="Booking QR Code" class="mx-auto mb-4" />
                <Button size="sm" variant="outline" on:click={downloadQRCode}>
                  Download QR Code
                </Button>
              </div>
            </Card>
            
            <!-- Timeline -->
            <Card title="Activity Timeline">
              <div class="flow-root">
                <ul class="-mb-8">
                  <li>
                    <div class="relative pb-8">
                      <span class="absolute left-4 top-4 -ml-px h-full w-0.5 bg-gray-200"></span>
                      <div class="relative flex space-x-3">
                        <div class="flex h-8 w-8 items-center justify-center rounded-full bg-green-500">
                          <svg class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                          </svg>
                        </div>
                        <div class="flex-1 space-y-1">
                          <p class="text-sm text-gray-900">Booking created</p>
                          <p class="text-xs text-gray-500">
                            {new Date(booking.created_at).toLocaleString()}
                          </p>
                        </div>
                      </div>
                    </div>
                  </li>
                  
                  {#if booking.confirmed_at}
                    <li>
                      <div class="relative pb-8">
                        <div class="relative flex space-x-3">
                          <div class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500">
                            <svg class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                            </svg>
                          </div>
                          <div class="flex-1 space-y-1">
                            <p class="text-sm text-gray-900">Booking confirmed</p>
                            <p class="text-xs text-gray-500">
                              {new Date(booking.confirmed_at).toLocaleString()}
                            </p>
                          </div>
                        </div>
                      </div>
                    </li>
                  {/if}
                </ul>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Cancel Modal -->
    <Modal bind:open={showCancelModal} title="Cancel Booking" size="md">
      <Alert type="warning">
        Are you sure you want to cancel this booking? This action cannot be undone.
      </Alert>
      
      <div slot="footer" class="flex justify-end gap-3">
        <Button variant="outline" on:click={() => showCancelModal = false}>
          Keep Booking
        </Button>
        <Button variant="danger" on:click={handleCancel} loading={updating}>
          Cancel Booking
        </Button>
      </div>
    </Modal>
    
    <!-- Reschedule Modal -->
    <Modal bind:open={showRescheduleModal} title="Reschedule Booking" size="md">
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            New Date
          </label>
          <input
            type="date"
            bind:value={newDate}
            min={new Date().toISOString().split('T')[0]}
            class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            New Time
          </label>
          <input
            type="time"
            bind:value={newTime}
            class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
          />
        </div>
      </div>
      
      <div slot="footer" class="flex justify-end gap-3">
        <Button variant="outline" on:click={() => showRescheduleModal = false}>
          Cancel
        </Button>
        <Button on:click={handleReschedule} loading={updating}>
          Reschedule
        </Button>
      </div>
    </Modal>
    
    <!-- Notes Modal -->
    <Modal bind:open={showNotesModal} title="Add Notes" size="md">
      <textarea
        bind:value={additionalNotes}
        rows="4"
        class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        placeholder="Enter notes..."
      ></textarea>
      
      <div slot="footer" class="flex justify-end gap-3">
        <Button variant="outline" on:click={() => showNotesModal = false}>
          Cancel
        </Button>
        <Button on:click={handleAddNotes} loading={updating}>
          Add Notes
        </Button>
      </div>
    </Modal>
  {/if}
  
  <style>
    @media print {
      :global(body) * {
        visibility: hidden;
      }
      
      .print-area, .print-area * {
        visibility: visible;
      }
      
      .print-area {
        position: absolute;
        left: 0;
        top: 0;
      }
    }
  </style>