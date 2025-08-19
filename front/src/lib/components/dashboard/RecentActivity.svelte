<!-- src/lib/components/dashboard/RecentActivity.svelte -->
<script>
    import { formatRelativeTime, formatCurrency } from '$lib/utils/formatters';
    import Card from '../common/Card.svelte';
    import Avatar from '../common/Avatar.svelte';
    import BookingStatus from '../booking/BookingStatus.svelte';
    import StarRating from '../review/StarRating.svelte';
    import Spinner from '../common/Spinner.svelte';
    import { goto } from '$app/navigation';
    
    let {
        activities = [],
        loading = false,
        showViewAll = true,
        maxItems = 10,
        ...restProps
    } = $props();
    
    const activityIcons = {
      booking_created: {
        icon: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
        color: 'bg-blue-100 text-blue-600'
      },
      booking_confirmed: {
        icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
        color: 'bg-green-100 text-green-600'
      },
      booking_cancelled: {
        icon: 'M6 18L18 6M6 6l12 12',
        color: 'bg-red-100 text-red-600'
      },
      booking_completed: {
        icon: 'M5 13l4 4L19 7',
        color: 'bg-green-100 text-green-600'
      },
      review_received: {
        icon: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z',
        color: 'bg-yellow-100 text-yellow-600'
      },
      payment_received: {
        icon: 'M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z',
        color: 'bg-green-100 text-green-600'
      },
      customer_joined: {
        icon: 'M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z',
        color: 'bg-purple-100 text-purple-600'
      },
      service_added: {
        icon: 'M12 4v16m8-8H4',
        color: 'bg-indigo-100 text-indigo-600'
      }
    };
    
    function getActivityIcon(type) {
      return activityIcons[type] || activityIcons.booking_created;
    }
    
    function handleActivityClick(activity) {
      if (activity.link) {
        goto(activity.link);
      }
    }
    
    let displayedActivities = $derived(activities.slice(0, maxItems));
  </script>
  
  <Card>
    {#snippet header()}
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">Recent Activity</h3>
        {#if showViewAll && activities.length > maxItems}
          <a href="/activities" class="text-sm text-indigo-600 hover:text-indigo-500">
            View all
          </a>
        {/if}
      </div>
    {/snippet}
    
    {#if loading}
      <div class="p-6">
        <Spinner>Loading activities...</Spinner>
      </div>
    {:else if displayedActivities.length > 0}
      <div class="flow-root">
        <ul class="-mb-8">
          {#each displayedActivities as activity, index}
            <li>
              <div class="relative pb-8">
                {#if index !== displayedActivities.length - 1}
                  <span 
                    class="absolute left-5 top-5 -ml-px h-full w-0.5 bg-gray-200" 
                    aria-hidden="true"
                  ></span>
                {/if}
                
                <div class="relative flex items-start space-x-3 hover:bg-gray-50 px-4 py-2 -mx-4 rounded-lg transition-colors">
                  <div class="relative">
                    {#if activity.user_avatar || activity.customer_avatar}
                      <Avatar
                        src={activity.user_avatar || activity.customer_avatar}
                        name={activity.user_name || activity.customer_name}
                        size="sm"
                      />
                    {:else}
                      {@const icon = getActivityIcon(activity.type)}
                      <div class="h-10 w-10 rounded-full flex items-center justify-center {icon.color}">
                        <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={icon.icon} />
                        </svg>
                      </div>
                    {/if}
                  </div>
                  
                  <div class="min-w-0 flex-1">
                    <div>
                      <p class="text-sm text-gray-900">
                        {#if activity.type === 'booking_created'}
                          <span class="font-medium">{activity.customer_name}</span> booked
                          <span class="font-medium">{activity.service_name}</span>
                          {#if activity.booking_date}
                            for {activity.booking_date}
                          {/if}
                        {:else if activity.type === 'booking_confirmed'}
                          Booking <span class="font-medium">#{activity.booking_id?.slice(0, 8)}</span> confirmed
                        {:else if activity.type === 'booking_cancelled'}
                          Booking <span class="font-medium">#{activity.booking_id?.slice(0, 8)}</span> cancelled
                        {:else if activity.type === 'booking_completed'}
                          <span class="font-medium">{activity.service_name}</span> completed for
                          <span class="font-medium">{activity.customer_name}</span>
                        {:else if activity.type === 'review_received'}
                          <span class="font-medium">{activity.customer_name}</span> left a
                          <StarRating rating={activity.rating} size="xs" /> review
                        {:else if activity.type === 'payment_received'}
                          Payment of <span class="font-medium">{formatCurrency(activity.amount)}</span> received
                        {:else if activity.type === 'customer_joined'}
                          <span class="font-medium">{activity.customer_name}</span> joined as a new customer
                        {:else if activity.type === 'service_added'}
                          New service <span class="font-medium">{activity.service_name}</span> added
                        {:else}
                          {activity.description}
                        {/if}
                      </p>
                      
                      <div class="mt-1 flex items-center space-x-2">
                        <p class="text-xs text-gray-500">
                          {formatRelativeTime(activity.created_at)}
                        </p>
                        
                        {#if activity.status}
                          <BookingStatus status={activity.status} size="xs" showIcon={false} />
                        {/if}
                        
                        {#if activity.link}
                          <button
                            type="button"
                            class="text-xs text-indigo-600 hover:text-indigo-500"
                            on:click={() => handleActivityClick(activity)}
                          >
                            View →
                          </button>
                        {/if}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          {/each}
        </ul>
      </div>
    {:else}
      <div class="p-6 text-center text-sm text-gray-500">
        <svg class="mx-auto h-12 w-12 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        No recent activity
      </div>
    {/if}
  </Card>