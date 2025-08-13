<!-- src/lib/components/review/ReviewList.svelte -->
<script>
    import { createEventDispatcher, onMount } from 'svelte';
    import { reviewAPI } from '$lib/api/reviews';
    import ReviewCard from './ReviewCard.svelte';
    import StarRating from './StarRating.svelte';
    import Select from '../common/Select.svelte';
    import Button from '../common/Button.svelte';
    import Spinner from '../common/Spinner.svelte';
    import Card from '../common/Card.svelte';
    
    export let businessId = null;
    export let reviews = [];
    export let loading = false;
    export let showActions = false;
    export let isBusinessOwner = false;
    export let showStats = true;
    export let compact = false;
    
    const dispatch = createEventDispatcher();
    
    let stats = null;
    let filteredReviews = [];
    let sortBy = 'recent';
    let filterRating = '';
    let filterVerified = false;
    let filterWithPhotos = false;
    let currentPage = 1;
    let reviewsPerPage = 10;
    
    $: totalPages = Math.ceil(filteredReviews.length / reviewsPerPage);
    $: paginatedReviews = filteredReviews.slice(
      (currentPage - 1) * reviewsPerPage,
      currentPage * reviewsPerPage
    );
    
    onMount(async () => {
      if (businessId && showStats) {
        const { data } = await reviewAPI.getStats(businessId);
        if (data) {
          stats = data;
        }
      }
      filterAndSortReviews();
    });
    
    $: filterAndSortReviews(), reviews, sortBy, filterRating, filterVerified, filterWithPhotos;
    
    function filterAndSortReviews() {
      let filtered = [...reviews];
      
      // Apply filters
      if (filterRating) {
        filtered = filtered.filter(r => r.rating === parseInt(filterRating));
      }
      
      if (filterVerified) {
        filtered = filtered.filter(r => r.is_verified);
      }
      
      if (filterWithPhotos) {
        filtered = filtered.filter(r => r.images && r.images.length > 0);
      }
      
      // Apply sorting
      switch (sortBy) {
        case 'recent':
          filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
          break;
        case 'oldest':
          filtered.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
          break;
        case 'highest':
          filtered.sort((a, b) => b.rating - a.rating);
          break;
        case 'lowest':
          filtered.sort((a, b) => a.rating - b.rating);
          break;
        case 'helpful':
          filtered.sort((a, b) => (b.helpful_count || 0) - (a.helpful_count || 0));
          break;
      }
      
      filteredReviews = filtered;
      currentPage = 1; // Reset to first page when filters change
    }
    
    function handlePageChange(page) {
      currentPage = page;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  </script>
  
  <div class="space-y-6">
    <!-- Stats Overview -->
    {#if showStats && stats}
      <Card>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Overall Rating -->
          <div class="text-center lg:text-left">
            <div class="flex items-center justify-center lg:justify-start space-x-4">
              <div>
                <div class="text-4xl font-bold text-gray-900">
                  {stats.average_rating ? stats.average_rating.toFixed(1) : '0.0'}
                </div>
                <StarRating rating={stats.average_rating || 0} size="md" />
                <p class="text-sm text-gray-500 mt-1">
                  Based on {stats.total_reviews || 0} reviews
                </p>
              </div>
            </div>
          </div>
          
          <!-- Rating Distribution -->
          <div class="lg:col-span-2">
            <div class="space-y-2">
              {#each [5, 4, 3, 2, 1] as rating}
                {@const count = stats[`rating_${rating}`] || 0}
                {@const percentage = stats.total_reviews > 0 ? (count / stats.total_reviews) * 100 : 0}
                <div class="flex items-center space-x-3">
                  <button
                    type="button"
                    class="flex items-center space-x-1 min-w-[60px] hover:text-indigo-600"
                    on:click={() => filterRating = filterRating === String(rating) ? '' : String(rating)}
                  >
                    <span class="text-sm font-medium">{rating}</span>
                    <svg class="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.957a1 1 0 00.95.69h4.162c.969 0 1.371 1.24.588 1.81l-3.37 2.448a1 1 0 00-.364 1.118l1.287 3.957c.3.921-.755 1.688-1.54 1.118l-3.37-2.448a1 1 0 00-1.175 0l-3.37 2.448c-.784.57-1.838-.197-1.539-1.118l1.287-3.957a1 1 0 00-.364-1.118L2.05 9.384c-.783-.57-.38-1.81.588-1.81h4.162a1 1 0 00.95-.69l1.286-3.957z" />
                    </svg>
                  </button>
                  
                  <div class="flex-1">
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div
                        class="bg-yellow-400 h-2 rounded-full transition-all duration-300"
                        style="width: {percentage}%"
                      ></div>
                    </div>
                  </div>
                  
                  <span class="text-sm text-gray-600 min-w-[40px] text-right">
                    {count}
                  </span>
                </div>
              {/each}
            </div>
            
            <!-- Recommendation Rate -->
            {#if stats.recommend_percentage !== undefined}
              <div class="mt-4 pt-4 border-t border-gray-200">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-600">Would recommend</span>
                  <span class="text-sm font-medium text-gray-900">
                    {stats.recommend_percentage}% of reviewers
                  </span>
                </div>
              </div>
            {/if}
          </div>
        </div>
      </Card>
    {/if}
    
    <!-- Filters and Sorting -->
    <Card>
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h3 class="text-lg font-semibold text-gray-900">
          Customer Reviews ({filteredReviews.length})
        </h3>
        
        <div class="flex flex-wrap items-center gap-3">
          <!-- Filter Chips -->
          <div class="flex flex-wrap gap-2">
            <label class="inline-flex items-center">
              <input
                type="checkbox"
                bind:checked={filterVerified}
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <span class="ml-2 text-sm text-gray-700">Verified only</span>
            </label>
            
            <label class="inline-flex items-center">
              <input
                type="checkbox"
                bind:checked={filterWithPhotos}
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <span class="ml-2 text-sm text-gray-700">With photos</span>
            </label>
          </div>
          
          <!-- Sort Dropdown -->
          <Select
            bind:value={sortBy}
            options={[
              { value: 'recent', label: 'Most Recent' },
              { value: 'oldest', label: 'Oldest First' },
              { value: 'highest', label: 'Highest Rated' },
              { value: 'lowest', label: 'Lowest Rated' },
              { value: 'helpful', label: 'Most Helpful' }
            ]}
          />
          
          {#if filterRating}
            <Button
              size="sm"
              variant="outline"
              on:click={() => filterRating = ''}
            >
              Clear {filterRating}★ filter
            </Button>
          {/if}
        </div>
      </div>
    </Card>
    
    <!-- Reviews List -->
    {#if loading}
      <div class="flex justify-center py-12">
        <Spinner size="lg">Loading reviews...</Spinner>
      </div>
    {:else if paginatedReviews.length > 0}
      <div class="space-y-4">
        {#each paginatedReviews as review (review.id)}
          <ReviewCard
            {review}
            {showActions}
            {isBusinessOwner}
            {compact}
            on:responded
            on:featured
            on:edit
            on:delete
            on:share
            on:viewImage
          />
        {/each}
      </div>
      
      <!-- Pagination -->
      {#if totalPages > 1}
        <div class="flex items-center justify-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            disabled={currentPage === 1}
            on:click={() => handlePageChange(currentPage - 1)}
          >
            Previous
          </Button>
          
          {#each Array(Math.min(5, totalPages)) as _, i}
            {@const page = currentPage <= 3 ? i + 1 : currentPage + i - 2}
            {#if page > 0 && page <= totalPages}
              <button
                type="button"
                class="
                  px-3 py-1 text-sm rounded-md
                  {page === currentPage 
                    ? 'bg-indigo-600 text-white' 
                    : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'}
                "
                on:click={() => handlePageChange(page)}
              >
                {page}
              </button>
            {/if}
          {/each}
          
          <Button
            variant="outline"
            size="sm"
            disabled={currentPage === totalPages}
            on:click={() => handlePageChange(currentPage + 1)}
          >
            Next
          </Button>
        </div>
      {/if}
    {:else}
      <Card>
        <div class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">No reviews yet</h3>
          <p class="mt-1 text-sm text-gray-500">
            {filterRating || filterVerified || filterWithPhotos
              ? 'No reviews match your filters'
              : 'Be the first to leave a review'}
          </p>
          {#if filterRating || filterVerified || filterWithPhotos}
            <div class="mt-4">
              <Button
                variant="outline"
                on:click={() => {
                  filterRating = '';
                  filterVerified = false;
                  filterWithPhotos = false;
                }}
              >
                Clear Filters
              </Button>
            </div>
          {/if}
        </div>
      </Card>
    {/if}
  </div>