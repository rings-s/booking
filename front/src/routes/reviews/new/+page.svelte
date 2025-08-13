<!-- src/routes/reviews/new/+page.svelte -->
<script>
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { reviewAPI } from '$lib/api/reviews';
  import { auth } from '$lib/stores/auth';
  import Input from '$lib/components/common/Input.svelte';
  import Button from '$lib/components/common/Button.svelte';
  import Alert from '$lib/components/common/Alert.svelte';
  import { validateForm, reviewSchema } from '$lib/utils/validators';
  import toast from 'svelte-french-toast';
  
  // Get business info from URL params
  const businessSlug = $page.url.searchParams.get('business');
  const bookingId = $page.url.searchParams.get('booking');
  
  let formData = {
    rating: 0,
    title: '',
    comment: '',
    business_slug: businessSlug,
    booking_id: bookingId
  };
  
  let loading = false;
  let errors = {};
  let hoveredRating = 0;
  
  // Check if user is authenticated
  $: if (!$auth.user) {
    goto(`/auth/login?redirect=${encodeURIComponent('/reviews/new')}`);
  }
  
  function setRating(rating) {
    formData.rating = rating;
    delete errors.rating;
  }
  
  function onRatingHover(rating) {
    hoveredRating = rating;
  }
  
  function onRatingLeave() {
    hoveredRating = 0;
  }
  
  async function handleSubmit() {
    loading = true;
    
    // Validate form
    const validation = await validateForm(reviewSchema, formData);
    if (!validation.isValid) {
      errors = validation.errors;
      loading = false;
      return;
    }
    
    // Submit review
    const { data, error } = await reviewAPI.create(formData);
    
    if (data) {
      toast.success('Review submitted successfully!');
      // Redirect to business page or booking history
      if (businessSlug) {
        goto(`/businesses/${businessSlug}`);
      } else {
        goto('/bookings');
      }
    } else {
      errors.general = error || 'Failed to submit review';
      toast.error(errors.general);
    }
    
    loading = false;
  }
  
  function getRatingText(rating) {
    const texts = {
      1: 'Poor',
      2: 'Fair', 
      3: 'Good',
      4: 'Very Good',
      5: 'Excellent'
    };
    return texts[rating] || 'Rate your experience';
  }
</script>

<svelte:head>
  <title>Write a Review - BookingPro</title>
</svelte:head>

<div class="min-h-screen bg-gray-50 py-12">
  <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="text-center mb-8">
      <h1 class="text-3xl font-bold text-gray-900">Write a Review</h1>
      <p class="mt-2 text-gray-600">
        Share your experience to help other customers make informed decisions
      </p>
    </div>
    
    <!-- Error Alert -->
    {#if errors.general}
      <Alert type="error" dismissible on:dismiss={() => errors.general = null}>
        {errors.general}
      </Alert>
    {/if}
    
    <!-- Review Form -->
    <div class="bg-white shadow-lg rounded-2xl p-8">
      <form on:submit|preventDefault={handleSubmit} class="space-y-6">
        <!-- Rating -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-3">
            Rating <span class="text-red-500">*</span>
          </label>
          
          <div class="flex items-center space-x-2">
            {#each [1, 2, 3, 4, 5] as star}
              <button
                type="button"
                on:click={() => setRating(star)}
                on:mouseenter={() => onRatingHover(star)}
                on:mouseleave={onRatingLeave}
                class="p-1 rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-yellow-400"
              >
                <svg 
                  class="w-10 h-10 transition-colors {
                    star <= (hoveredRating || formData.rating) 
                      ? 'text-yellow-400' 
                      : 'text-gray-300'
                  }" 
                  fill="currentColor" 
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </button>
            {/each}
            
            <span class="ml-4 text-sm font-medium text-gray-600">
              {getRatingText(hoveredRating || formData.rating)}
            </span>
          </div>
          
          {#if errors.rating}
            <p class="mt-1 text-sm text-red-600">{errors.rating}</p>
          {/if}
        </div>
        
        <!-- Review Title -->
        <Input
          label="Review Title"
          bind:value={formData.title}
          error={errors.title}
          placeholder="Summarize your experience"
          required
        />
        
        <!-- Review Comment -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Your Review <span class="text-red-500">*</span>
          </label>
          <textarea
            bind:value={formData.comment}
            rows="6"
            class="
              block w-full rounded-lg shadow-sm sm:text-sm
              {errors.comment 
                ? 'border-red-300 text-red-900 focus:border-red-500 focus:ring-red-500' 
                : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'}
            "
            placeholder="Tell others about your experience. What did you like? What could be improved?"
          ></textarea>
          {#if errors.comment}
            <p class="mt-1 text-sm text-red-600">{errors.comment}</p>
          {/if}
          
          <div class="mt-2 text-sm text-gray-500">
            {formData.comment.length}/1000 characters
          </div>
        </div>
        
        <!-- Guidelines -->
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 class="text-sm font-medium text-blue-900 mb-2">Review Guidelines</h4>
          <ul class="text-sm text-blue-800 space-y-1">
            <li>• Be honest and provide constructive feedback</li>
            <li>• Focus on your personal experience</li>
            <li>• Avoid inappropriate language or personal attacks</li>
            <li>• Include specific details about the service</li>
          </ul>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center justify-between pt-6">
          <Button
            variant="outline"
            on:click={() => window.history.back()}
            type="button"
          >
            Cancel
          </Button>
          
          <Button
            type="submit"
            {loading}
            disabled={!formData.rating || loading}
          >
            Submit Review
          </Button>
        </div>
      </form>
    </div>
    
    <!-- Trust & Safety -->
    <div class="mt-8 text-center">
      <div class="inline-flex items-center text-sm text-gray-500">
        <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
        Your review will be published after moderation
      </div>
    </div>
  </div>
</div>