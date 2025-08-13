<!-- src/lib/components/review/ReviewCard.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
    import { formatDate, formatRelativeTime } from '$lib/utils/formatters';
    import StarRating from './StarRating.svelte';
    import Avatar from '../common/Avatar.svelte';
    import Button from '../common/Button.svelte';
    import Modal from '../common/Modal.svelte';
    import { reviewAPI } from '$lib/api/reviews';
    import toast from 'svelte-french-toast';
    
    export let review;
    export let showActions = false;
    export let isBusinessOwner = false;
    export let compact = false;
    
    const dispatch = createEventDispatcher();
    
    let showResponseModal = false;
    let responseText = '';
    let responding = false;
    let showReportModal = false;
    let reportReason = '';
    let reporting = false;
    let helpful = review.helpful_count || 0;
    let hasVoted = false;
    
    async function handleRespond() {
      if (!responseText.trim()) {
        toast.error('Please write a response');
        return;
      }
      
      responding = true;
      const { error } = await reviewAPI.respond(review.id, responseText);
      
      if (!error) {
        review.business_response = responseText;
        review.response_date = new Date().toISOString();
        showResponseModal = false;
        toast.success('Response posted successfully');
        dispatch('responded', review);
      }
      responding = false;
    }
    
    async function handleFeature() {
      const { error } = await reviewAPI.markFeatured(review.id);
      
      if (!error) {
        review.is_featured = true;
        toast.success('Review marked as featured');
        dispatch('featured', review);
      }
    }
    
    async function handleHelpful() {
      if (hasVoted) return;
      
      const { error } = await reviewAPI.markHelpful(review.id);
      
      if (!error) {
        helpful++;
        hasVoted = true;
        toast.success('Thanks for your feedback');
      }
    }
    
    async function handleReport() {
      if (!reportReason.trim()) {
        toast.error('Please provide a reason');
        return;
      }
      
      reporting = true;
      const { error } = await reviewAPI.report(review.id, reportReason);
      
      if (!error) {
        showReportModal = false;
        toast.success('Review reported. We\'ll look into it.');
      }
      reporting = false;
    }
    
    function handleEdit() {
      dispatch('edit', review);
    }
    
    function handleDelete() {
      if (confirm('Are you sure you want to delete this review?')) {
        dispatch('delete', review);
      }
    }
  </script>
  
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 {compact ? 'p-4' : 'p-6'}">
    <div class="flex items-start space-x-4">
      <!-- Customer Avatar -->
      <div class="flex-shrink-0">
        <Avatar
          name={review.customer.user.full_name}
          src={review.customer.user.avatar}
          size={compact ? 'sm' : 'md'}
        />
      </div>
      
      <!-- Review Content -->
      <div class="flex-1 min-w-0">
        <!-- Header -->
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center space-x-2">
              <h4 class="text-sm font-semibold text-gray-900">
                {review.customer.user.full_name}
              </h4>
              
              {#if review.is_verified}
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                  <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  Verified Purchase
                </span>
              {/if}
              
              {#if review.is_featured}
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                  <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.957a1 1 0 00.95.69h4.162c.969 0 1.371 1.24.588 1.81l-3.37 2.448a1 1 0 00-.364 1.118l1.287 3.957c.3.921-.755 1.688-1.54 1.118l-3.37-2.448a1 1 0 00-1.175 0l-3.37 2.448c-.784.57-1.838-.197-1.539-1.118l1.287-3.957a1 1 0 00-.364-1.118L2.05 9.384c-.783-.57-.38-1.81.588-1.81h4.162a1 1 0 00.95-.69l1.286-3.957z" />
                  </svg>
                  Featured
                </span>
              {/if}
            </div>
            
            <div class="mt-1 flex items-center space-x-3">
              <StarRating rating={review.rating} size="sm" />
              <time class="text-xs text-gray-500">
                {formatRelativeTime(review.created_at)}
              </time>
            </div>
          </div>
          
          {#if showActions && !compact}
            <div class="relative">
              <button
                type="button"
                class="text-gray-400 hover:text-gray-500"
                on:click={() => dispatch('menu', review)}
              >
                <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                </svg>
              </button>
            </div>
          {/if}
        </div>
        
        <!-- Review Title & Content -->
        {#if review.title && !compact}
          <h3 class="mt-2 text-base font-medium text-gray-900">{review.title}</h3>
        {/if}
        
        <p class="mt-2 text-sm text-gray-600 {compact ? 'line-clamp-2' : ''}">
          {review.comment}
        </p>
        
        <!-- Service & Booking Info -->
        {#if review.booking && !compact}
          <div class="mt-3 flex items-center text-xs text-gray-500">
            <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            {review.booking.service.name} • {formatDate(review.booking.booking_date)}
          </div>
        {/if}
        
        <!-- Review Images if any -->
        {#if review.images && review.images.length > 0 && !compact}
          <div class="mt-3 flex space-x-2">
            {#each review.images.slice(0, 4) as image, index}
              <button
                type="button"
                class="relative w-20 h-20 rounded-lg overflow-hidden group"
                on:click={() => dispatch('viewImage', { review, imageIndex: index })}
              >
                <img
                  src={image.thumbnail || image.url}
                  alt="Review image {index + 1}"
                  class="w-full h-full object-cover group-hover:opacity-75 transition-opacity"
                />
                {#if index === 3 && review.images.length > 4}
                  <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                    <span class="text-white text-sm font-medium">+{review.images.length - 4}</span>
                  </div>
                {/if}
              </button>
            {/each}
          </div>
        {/if}
        
        <!-- Business Response -->
        {#if review.business_response}
          <div class="mt-4 p-3 bg-gray-50 rounded-lg border border-gray-200">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center">
                {#if review.business.logo}
                  <img
                    src={review.business.logo}
                    alt={review.business.name}
                    class="w-6 h-6 rounded-full mr-2"
                  />
                {/if}
                <span class="text-sm font-medium text-gray-900">Business Response</span>
              </div>
              <time class="text-xs text-gray-500">
                {formatRelativeTime(review.response_date)}
              </time>
            </div>
            <p class="text-sm text-gray-600">{review.business_response}</p>
          </div>
        {/if}
        
        <!-- Actions Bar -->
        {#if !compact}
          <div class="mt-4 flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <!-- Helpful Button -->
              <button
                type="button"
                class="flex items-center text-sm text-gray-500 hover:text-gray-700"
                on:click={handleHelpful}
                disabled={hasVoted}
              >
                <svg class="w-4 h-4 mr-1 {hasVoted ? 'text-green-600' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                </svg>
                Helpful {helpful > 0 ? `(${helpful})` : ''}
              </button>
              
              <!-- Share Button -->
              <button
                type="button"
                class="flex items-center text-sm text-gray-500 hover:text-gray-700"
                on:click={() => dispatch('share', review)}
              >
                <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m9.032 4.026a3 3 0 10-4.732 0m-9.032-4.026A3 3 0 108.684 6.632m0 6.736a3 3 0 00-4.732 0" />
                </svg>
                Share
              </button>
              
              <!-- Report Button -->
              {#if !isBusinessOwner}
                <button
                  type="button"
                  class="flex items-center text-sm text-gray-500 hover:text-gray-700"
                  on:click={() => showReportModal = true}
                >
                  <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9" />
                  </svg>
                  Report
                </button>
              {/if}
            </div>
            
            <!-- Business Owner Actions -->
            {#if showActions && isBusinessOwner}
              <div class="flex items-center space-x-2">
                {#if !review.business_response}
                  <Button
                    size="sm"
                    variant="outline"
                    on:click={() => showResponseModal = true}
                  >
                    Respond
                  </Button>
                {/if}
                
                {#if !review.is_featured}
                  <Button
                    size="sm"
                    variant="outline"
                    on:click={handleFeature}
                  >
                    Feature
                  </Button>
                {/if}
              </div>
            {/if}
          </div>
        {/if}
      </div>
    </div>
  </div>
  
  <!-- Response Modal -->
  <Modal bind:open={showResponseModal} title="Respond to Review" size="md">
    <div class="space-y-4">
      <div class="bg-gray-50 rounded-lg p-4">
        <div class="flex items-center mb-2">
          <StarRating rating={review.rating} size="sm" />
          <span class="ml-2 text-sm text-gray-600">by {review.customer.user.full_name}</span>
        </div>
        <p class="text-sm text-gray-600">{review.comment}</p>
      </div>
      
      <div>
        <label for="response" class="block text-sm font-medium text-gray-700 mb-1">
          Your Response
        </label>
        <textarea
          id="response"
          bind:value={responseText}
          rows="4"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          placeholder="Thank you for your feedback..."
        ></textarea>
        <p class="mt-1 text-xs text-gray-500">
          {responseText.length}/500 characters
        </p>
      </div>
    </div>
    
    <div slot="footer" class="flex justify-end gap-3">
      <Button variant="outline" on:click={() => showResponseModal = false}>
        Cancel
      </Button>
      <Button on:click={handleRespond} loading={responding}>
        Post Response
      </Button>
    </div>
  </Modal>
  
  <!-- Report Modal -->
  <Modal bind:open={showReportModal} title="Report Review" size="md">
    <div class="space-y-4">
      <Alert type="info">
        Please let us know why you're reporting this review. We'll investigate and take appropriate action.
      </Alert>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          Reason for reporting
        </label>
        <div class="space-y-2">
          {#each ['Inappropriate content', 'Fake review', 'Spam', 'Offensive language', 'Other'] as reason}
            <label class="flex items-center">
              <input
                type="radio"
                bind:group={reportReason}
                value={reason}
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300"
              />
              <span class="ml-2 text-sm text-gray-700">{reason}</span>
            </label>
          {/each}
        </div>
      </div>
      
      {#if reportReason === 'Other'}
        <div>
          <label for="details" class="block text-sm font-medium text-gray-700 mb-1">
            Please provide details
          </label>
          <textarea
            id="details"
            rows="3"
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          ></textarea>
        </div>
      {/if}
    </div>
    
    <div slot="footer" class="flex justify-end gap-3">
      <Button variant="outline" on:click={() => showReportModal = false}>
        Cancel
      </Button>
      <Button variant="danger" on:click={handleReport} loading={reporting}>
        Report Review
      </Button>
    </div>
  </Modal>