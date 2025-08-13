<!-- src/routes/businesses/[slug]/+page.svelte -->
<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { businessAPI } from '$lib/api/businesses';
    import { bookingAPI } from '$lib/api/bookings';
    import { reviewAPI } from '$lib/api/reviews';
    import { auth } from '$lib/stores/auth';
    import Button from '$lib/components/common/Button.svelte';
    import ServiceList from '$lib/components/business/ServiceList.svelte';
    import ReviewList from '$lib/components/review/ReviewList.svelte';
    import ReviewForm from '$lib/components/review/ReviewForm.svelte';
    import BusinessHours from '$lib/components/business/BusinessHours.svelte';
    import QRCode from '$lib/components/business/QRCode.svelte';
    import BookingForm from '$lib/components/booking/BookingForm.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import toast from 'svelte-french-toast';
    
    export let data;
    
    let business = data.business;
    let services = data.services;
    let reviews = data.reviews;
    let loading = false;
    let activeTab = 'services';
    let showBookingModal = false;
    let selectedService = null;
    let showReviewModal = false;
    let showQRModal = false;
    let isFavorite = false;
    
    const slug = $page.params.slug;
    
    // Data is loaded from +page.js, so no onMount needed for initial load
    // But we can refresh data when needed
    async function loadReviews() {
      const { data } = await reviewAPI.getByBusiness(business?.id || business?.slug || slug);
      if (data) {
        reviews = data;
      }
    }
    
    async function toggleFavorite() {
      if (!$auth.isAuthenticated) {
        toast.error('Please login to save favorites');
        goto('/auth/login');
        return;
      }
      
      const { data, error } = isFavorite 
        ? await businessAPI.removeFavorite(business.id)
        : await businessAPI.addFavorite(business.id);
      
      if (data) {
        isFavorite = !isFavorite;
        toast.success(isFavorite ? 'Added to favorites' : 'Removed from favorites');
      }
    }
    
    function handleBookService(service) {
      console.log('handleBookService called with:', service);
      
      if (!$auth.isAuthenticated) {
        toast.error('Please login to book services');
        goto('/auth/login');
        return;
      }
      
      if (!service) {
        toast.error('No service selected');
        return;
      }
      
      selectedService = service;
      showBookingModal = true;
      console.log('Opening booking modal for service:', service.name);
      toast.success(`Booking ${service.name}...`);
    }
    
    function shareBusiness() {
      if (navigator.share) {
        navigator.share({
          title: business.name,
          text: business.description,
          url: window.location.href
        });
      } else {
        navigator.clipboard.writeText(window.location.href);
        toast.success('Link copied to clipboard');
      }
    }
  </script>
  
  {#if loading}
    <div class="min-h-screen flex items-center justify-center">
      <Spinner size="lg">Loading business details...</Spinner>
    </div>
  {:else if business}
    <div class="min-h-screen bg-gray-50">
      <!-- Hero Section -->
      <div class="relative h-96 bg-gradient-to-r from-indigo-600 to-purple-600">
        <!-- Cover Image -->
        {#if business.cover_image}
          <img 
            src={business.cover_image} 
            alt={business.name}
            class="absolute inset-0 w-full h-full object-cover opacity-30"
          />
        {/if}
        
        <!-- Overlay -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
        
        <!-- Content -->
        <div class="relative h-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-end pb-8">
          <div class="flex items-start justify-between w-full">
            <div class="flex items-start space-x-6">
              <!-- Logo -->
              {#if business.logo}
                <img 
                  src={business.logo} 
                  alt={business.name}
                  class="w-32 h-32 rounded-xl shadow-xl bg-white p-2"
                />
              {/if}
              
              <!-- Info -->
              <div class="text-white">
                <h1 class="text-4xl font-bold mb-2">{business.name}</h1>
                
                <!-- Rating -->
                <div class="flex items-center space-x-2 mb-2">
                  <div class="flex text-yellow-400">
                    {#each Array(5) as _, i}
                      <svg class="w-5 h-5 {i < Math.floor(business.average_rating || 0) ? 'fill-current' : 'fill-transparent'}" 
                           viewBox="0 0 20 20" stroke="currentColor">
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.957a1 1 0 00.95.69h4.162c.969 0 1.371 1.24.588 1.81l-3.37 2.448a1 1 0 00-.364 1.118l1.287 3.957c.3.921-.755 1.688-1.54 1.118l-3.37-2.448a1 1 0 00-1.175 0l-3.37 2.448c-.784.57-1.838-.197-1.539-1.118l1.287-3.957a1 1 0 00-.364-1.118L2.05 9.384c-.783-.57-.38-1.81.588-1.81h4.162a1 1 0 00.95-.69l1.286-3.957z" />
                      </svg>
                    {/each}
                  </div>
                  <span class="text-white">{business.average_rating?.toFixed(1) || 0}</span>
                  <span class="text-white/80">({business.review_count || 0} reviews)</span>
                </div>
                
                <!-- Location -->
                <div class="flex items-center text-white/80">
                  <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  {business.address}, {business.city}, {business.state}
                </div>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="flex items-center space-x-3">
              <Button
                variant="outline"
                class="bg-white/10 backdrop-blur-sm text-white border-white/30 hover:bg-white/20"
                on:click={toggleFavorite}
              >
                <svg class="w-5 h-5 {isFavorite ? 'fill-current' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </Button>
              
              <Button
                variant="outline"
                class="bg-white/10 backdrop-blur-sm text-white border-white/30 hover:bg-white/20"
                on:click={shareBusiness}
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m9.032 4.026a3 3 0 10-5.356 0m-9.032-4.026A5.002 5.002 0 0119.288 6m0 0A5.002 5.002 0 0115 7m4.288-1a3 3 0 10-4.026 1.797M9 13a3 3 0 110-6 3 3 0 010 6z" />
                </svg>
              </Button>
              
              <Button
                variant="outline"
                class="bg-white/10 backdrop-blur-sm text-white border-white/30 hover:bg-white/20"
                on:click={() => showQRModal = true}
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
                </svg>
              </Button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Navigation Tabs -->
      <div class="bg-white shadow-sm sticky top-0 z-10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex space-x-8">
            {#each ['services', 'about', 'reviews', 'hours'] as tab}
              <button
                class="py-4 px-1 border-b-2 font-medium text-sm transition-colors
                       {activeTab === tab 
                         ? 'border-indigo-500 text-indigo-600' 
                         : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
                on:click={() => activeTab = tab}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
                {#if tab === 'reviews'}
                  <span class="ml-2 px-2 py-0.5 text-xs bg-gray-100 text-gray-600 rounded-full">
                    {reviews.length}
                  </span>
                {/if}
              </button>
            {/each}
          </div>
        </div>
      </div>
      
      <!-- Content -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Main Content -->
          <div class="lg:col-span-2">
            {#if activeTab === 'services'}
              <div class="space-y-4">
                <h2 class="text-2xl font-bold text-gray-900 mb-6">Available Services</h2>
                {#if services.length === 0}
                  <p class="text-gray-500">No services available at the moment.</p>
                {:else}
                  <ServiceList 
                    {services}
                    on:book={(e) => handleBookService(e.detail)}
                  />
                {/if}
              </div>
            {:else if activeTab === 'about'}
              <div class="bg-white rounded-lg shadow-sm p-6">
                <h2 class="text-2xl font-bold text-gray-900 mb-4">About {business.name}</h2>
                <p class="text-gray-600 whitespace-pre-wrap">{business.description}</p>
                
                {#if business.amenities && business.amenities.length > 0}
                  <div class="mt-6">
                    <h3 class="text-lg font-semibold text-gray-900 mb-3">Amenities</h3>
                    <div class="flex flex-wrap gap-2">
                      {#each business.amenities as amenity}
                        <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                          {amenity}
                        </span>
                      {/each}
                    </div>
                  </div>
                {/if}
              </div>
            {:else if activeTab === 'reviews'}
              <div>
                {#if $auth.isAuthenticated}
                  <div class="mb-6 text-right">
                    <Button on:click={() => showReviewModal = true}>
                      Write a Review
                    </Button>
                  </div>
                {/if}
                
                <ReviewList 
                  businessId={business.id}
                  {reviews}
                />
              </div>
            {:else if activeTab === 'hours'}
              <BusinessHours 
                hours={business.business_hours || []}
                editable={false}
              />
            {/if}
          </div>
          
          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Quick Actions -->
            <div class="bg-white rounded-lg shadow-sm p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
              <div class="space-y-3">
                <Button fullWidth on:click={() => {
                  console.log('Book Now clicked', { 
                    isAuthenticated: $auth.isAuthenticated, 
                    servicesCount: services.length 
                  });
                  
                  if (!$auth.isAuthenticated) {
                    toast.error('Please login to book services');
                    goto('/auth/login');
                    return;
                  }
                  
                  if (services.length === 0) {
                    toast.error('No services available for booking');
                    return;
                  }
                  
                  if (services.length === 1) {
                    // If there's only one service, book it directly
                    console.log('Booking single service:', services[0]);
                    handleBookService(services[0]);
                  } else {
                    // If multiple services, switch to services tab
                    console.log('Multiple services, switching to services tab');
                    activeTab = 'services';
                    toast.success('Select a service below to book');
                  }
                }}>
                  Book Now
                </Button>
                
                <Button fullWidth variant="outline" href="tel:{business.phone}">
                  <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  Call {business.phone}
                </Button>
                
                <Button fullWidth variant="outline" on:click={() => window.open(`https://maps.google.com/?q=${business.address}`)}>
                  <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  Get Directions
                </Button>
              </div>
            </div>
            
            <!-- Contact Info -->
            <div class="bg-white rounded-lg shadow-sm p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
              <div class="space-y-3">
                <div class="flex items-start">
                  <svg class="w-5 h-5 text-gray-400 mt-0.5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <div class="text-sm">
                    <p class="text-gray-900">{business.address}</p>
                    <p class="text-gray-600">{business.city}, {business.state} {business.zip_code}</p>
                  </div>
                </div>
                
                {#if business.phone}
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                    <a href="tel:{business.phone}" class="text-sm text-indigo-600 hover:text-indigo-500">
                      {business.phone}
                    </a>
                  </div>
                {/if}
                
                {#if business.email}
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    <a href="mailto:{business.email}" class="text-sm text-indigo-600 hover:text-indigo-500">
                      {business.email}
                    </a>
                  </div>
                {/if}
                
                {#if business.website}
                  <div class="flex items-center">
                    <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                    </svg>
                    <a href={business.website} target="_blank" class="text-sm text-indigo-600 hover:text-indigo-500">
                      Visit Website
                    </a>
                  </div>
                {/if}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- QR Code Modal -->
    <Modal bind:open={showQRModal} title="Booking QR Code" size="md">
      <QRCode {business} showCustomization />
    </Modal>
    
    <!-- Review Modal -->
    <Modal bind:open={showReviewModal} title="Write a Review" size="lg">
      <ReviewForm 
        {business}
        on:success={() => {
          showReviewModal = false;
          loadReviews();
          toast.success('Review submitted successfully!');
        }}
        on:cancel={() => showReviewModal = false}
      />
    </Modal>
    
    <!-- Booking Modal -->
    <Modal bind:open={showBookingModal} title="Book Your Appointment" size="xl">
      <BookingForm 
        {business}
        service={selectedService}
        on:success={() => {
          showBookingModal = false;
          toast.success('Booking completed successfully!');
        }}
        on:cancel={() => showBookingModal = false}
      />
    </Modal>
  {/if}