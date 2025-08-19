<!-- src/lib/components/review/ReviewForm.svelte -->
<script>
    import { createEventDispatcher, onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import Input from '../common/Input.svelte';
    import Button from '../common/Button.svelte';
    import StarRating from './StarRating.svelte';
    import Alert from '../common/Alert.svelte';
    import Card from '../common/Card.svelte';
    import { validateForm, reviewSchema } from '$lib/utils/validators';
    import { reviewAPI } from '$lib/api/reviews';
    import toast from 'svelte-french-toast';
    
    let {
        booking = null,
        business = null,
        review = null, // For editing
        loading = false,
        ...restProps
    } = $props();
    
    const dispatch = createEventDispatcher();
    
    let formData = {
      rating: review?.rating || 0,
      title: review?.title || '',
      comment: review?.comment || '',
      business_id: business?.id || booking?.business?.id || review?.business?.id || '',
      booking_id: booking?.id || review?.booking?.id || '',
      recommend: review?.recommend !== false,
      anonymous: review?.anonymous || false
    };
    
    let errors = {};
    let images = [];
    let uploadingImages = false;
    let categoryRatings = {
      service: 0,
      value: 0,
      cleanliness: 0,
      communication: 0
    };
    
    // Predefined quick feedback options
    const quickFeedback = {
      5: ['Excellent service!', 'Highly recommended!', 'Amazing experience!'],
      4: ['Great service', 'Very satisfied', 'Would come again'],
      3: ['Good overall', 'Met expectations', 'Satisfactory'],
      2: ['Could be better', 'Below expectations', 'Needs improvement'],
      1: ['Poor experience', 'Very disappointed', 'Would not recommend']
    };
    
    onMount(() => {
      if (review) {
        categoryRatings = review.category_ratings || categoryRatings;
        images = review.images || [];
      }
    });
    
    function handleQuickFeedback(feedback) {
      formData.title = feedback;
    }
    
    async function handleImageUpload(event) {
      const files = event.target.files;
      if (!files || files.length === 0) return;
      
      uploadingImages = true;
      
      for (const file of files) {
        if (file.size > 5 * 1024 * 1024) {
          toast.error(`${file.name} is too large. Max size is 5MB`);
          continue;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
          images = [...images, {
            url: e.target.result,
            file: file,
            name: file.name
          }];
        };
        reader.readAsDataURL(file);
      }
      
      uploadingImages = false;
    }
    
    function removeImage(index) {
      images = images.filter((_, i) => i !== index);
    }
    
    async function handleSubmit() {
      // Custom validation
      if (formData.rating === 0) {
        errors.rating = 'Please select a rating';
        toast.error('Please select a rating');
        return;
      }
      
      const validation = await validateForm(reviewSchema, formData);
      
      if (!validation.isValid) {
        errors = validation.errors;
        toast.error('Please check all required fields');
        return;
      }
      
      loading = true;
      errors = {};
      
      // Prepare review data
      const reviewData = {
        ...formData,
        category_ratings: categoryRatings
      };
      
      // Handle image uploads if needed
      if (images.length > 0) {
        const formDataWithImages = new FormData();
        Object.keys(reviewData).forEach(key => {
          formDataWithImages.append(key, reviewData[key]);
        });
        
        images.forEach((image, index) => {
          if (image.file) {
            formDataWithImages.append(`image_${index}`, image.file);
          }
        });
        
        reviewData.images = images.map(img => img.url);
      }
      
      const { data, error } = review 
        ? await reviewAPI.update(review.id, reviewData)
        : await reviewAPI.create(reviewData);
      
      if (error) {
        toast.error(error);
      } else {
        toast.success(review ? 'Review updated successfully!' : 'Thank you for your review!');
        dispatch('success', data);
        
        // Redirect to business page
        if (business) {
          goto(`/businesses/${business.slug}`);
        } else if (booking) {
          goto(`/bookings/${booking.id}`);
        }
      }
      
      loading = false;
    }
    
    // Calculate overall rating from category ratings
    $effect(() => {
      if (Object.values(categoryRatings).some(r => r > 0)) {
        const validRatings = Object.values(categoryRatings).filter(r => r > 0);
        if (validRatings.length > 0) {
          formData.rating = Math.round(validRatings.reduce((a, b) => a + b, 0) / validRatings.length);
        }
      }
    });
    
    let suggestedFeedback = $derived(quickFeedback[formData.rating] || []);
  </script>
  
  <form on:submit|preventDefault={handleSubmit} class="max-w-2xl mx-auto space-y-6">
    {#if booking}
      <Alert type="info">
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium">Reviewing your experience</p>
            <p class="text-sm mt-1">
              {booking.service.name} at {booking.business.name}
            </p>
            <p class="text-xs mt-1 opacity-75">
              {new Date(booking.booking_date).toLocaleDateString()} at {booking.start_time}
            </p>
          </div>
          {#if booking.business.logo}
            <img
              src={booking.business.logo}
              alt={booking.business.name}
              class="w-12 h-12 rounded-lg object-cover"
            />
          {/if}
        </div>
      </Alert>
    {/if}
    
    <Card title="Overall Rating">
      <div class="text-center">
        <p class="text-sm text-gray-600 mb-4">
          How would you rate your overall experience?
        </p>
        <div class="flex justify-center mb-4">
          <StarRating
            bind:rating={formData.rating}
            interactive={true}
            size="lg"
          />
        </div>
        {#if formData.rating > 0}
          <p class="text-sm font-medium text-gray-700">
            {#if formData.rating === 5}
              Excellent! 🎉
            {:else if formData.rating === 4}
              Great! 😊
            {:else if formData.rating === 3}
              Good 👍
            {:else if formData.rating === 2}
              Fair 😐
            {:else}
              Poor 😞
            {/if}
          </p>
        {/if}
        {#if errors.rating}
          <p class="mt-2 text-sm text-red-600">{errors.rating}</p>
        {/if}
      </div>
    </Card>
    
    {#if formData.rating > 0}
      <Card title="Rate Specific Aspects" subtitle="Optional - Help others with detailed feedback">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Service Quality
            </label>
            <StarRating
              bind:rating={categoryRatings.service}
              interactive={true}
              size="sm"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Value for Money
            </label>
            <StarRating
              bind:rating={categoryRatings.value}
              interactive={true}
              size="sm"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Cleanliness
            </label>
            <StarRating
              bind:rating={categoryRatings.cleanliness}
              interactive={true}
              size="sm"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Communication
            </label>
            <StarRating
              bind:rating={categoryRatings.communication}
              interactive={true}
              size="sm"
            />
          </div>
        </div>
      </Card>
      
      <Card title="Write Your Review">
        <div class="space-y-4">
          <Input
            label="Review Title"
            bind:value={formData.title}
            error={errors.title}
            required
            placeholder="Summarize your experience"
          />
          
          {#if suggestedFeedback.length > 0}
            <div>
              <p class="text-xs text-gray-500 mb-2">Quick suggestions:</p>
              <div class="flex flex-wrap gap-2">
                {#each suggestedFeedback as feedback}
                  <button
                    type="button"
                    class="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700"
                    on:click={() => handleQuickFeedback(feedback)}
                  >
                    {feedback}
                  </button>
                {/each}
              </div>
            </div>
          {/if}
          
          <div>
            <label for="comment" class="block text-sm font-medium text-gray-700 mb-1">
              Your Review <span class="text-red-500">*</span>
            </label>
            <textarea
              id="comment"
              bind:value={formData.comment}
              rows="6"
              class="
                block w-full rounded-md shadow-sm sm:text-sm
                {errors.comment 
                  ? 'border-red-300 text-red-900 focus:border-red-500 focus:ring-red-500' 
                  : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'}
              "
              placeholder="Share details about your experience..."
            ></textarea>
            {#if errors.comment}
              <p class="mt-1 text-sm text-red-600">{errors.comment}</p>
            {/if}
            <div class="mt-1 flex justify-between text-xs text-gray-500">
              <span>{formData.comment.length}/1000 characters</span>
              <span>Min 10 characters required</span>
            </div>
          </div>
          
          <!-- Image Upload -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Add Photos (optional)
            </label>
            
            {#if images.length > 0}
              <div class="grid grid-cols-4 gap-2 mb-3">
                {#each images as image, index}
                  <div class="relative group">
                    <img
                      src={image.url}
                      alt="Review image {index + 1}"
                      class="w-full h-20 object-cover rounded-lg"
                    />
                    <button
                      type="button"
                      class="absolute top-1 right-1 p-1 bg-red-600 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                      on:click={() => removeImage(index)}
                    >
                      <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                {/each}
              </div>
            {/if}
            
            <label class="
              flex items-center justify-center px-4 py-2
              border-2 border-dashed border-gray-300 rounded-lg
              hover:border-gray-400 cursor-pointer
            ">
              <input
                type="file"
                accept="image/*"
                multiple
                class="hidden"
                on:change={handleImageUpload}
                disabled={uploadingImages || images.length >= 5}
              />
              <svg class="w-5 h-5 mr-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <span class="text-sm text-gray-600">
                {images.length >= 5 ? 'Max 5 images' : 'Add photos'}
              </span>
            </label>
            
            {#if uploadingImages}
              <p class="mt-2 text-sm text-gray-500">Uploading images...</p>
            {/if}
          </div>
          
          <!-- Additional Options -->
          <div class="space-y-3 pt-4 border-t border-gray-200">
            <label class="flex items-center">
              <input
                type="checkbox"
                bind:checked={formData.recommend}
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <span class="ml-2 text-sm text-gray-700">
                I would recommend this to others
              </span>
            </label>
            
            <label class="flex items-center">
              <input
                type="checkbox"
                bind:checked={formData.anonymous}
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <span class="ml-2 text-sm text-gray-700">
                Post as anonymous
              </span>
            </label>
          </div>
        </div>
      </Card>
    {/if}
    
    <div class="flex justify-between">
      <Button variant="outline" type="button" on:click={() => dispatch('cancel')}>
        Cancel
      </Button>
      <Button type="submit" {loading} disabled={formData.rating === 0}>
        {review ? 'Update' : 'Submit'} Review
      </Button>
    </div>
  </form>