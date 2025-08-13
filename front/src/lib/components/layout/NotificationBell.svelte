<!-- src/lib/components/layout/NotificationBell.svelte -->
<script>
    import { onMount, onDestroy } from 'svelte';
    import { notificationStore, unreadCount } from '$lib/stores/notification';
    import { isAuthenticated } from '$lib/stores/auth';
    import { formatRelativeTime } from '$lib/utils/formatters';
    
    let showDropdown = false;
    let notifications = [];
    let unsubscribe = null;
    
    onMount(() => {
      // Only poll if authenticated
      if ($isAuthenticated) {
        notificationStore.startPolling();
      }
      
      unsubscribe = notificationStore.subscribe(state => {
        notifications = state.notifications.slice(0, 5);
      });
      
      // Watch authentication state
      const authUnsubscribe = isAuthenticated.subscribe(authenticated => {
        if (authenticated) {
          notificationStore.startPolling();
        } else {
          notificationStore.stopPolling();
        }
      });
      
      return () => {
        if (unsubscribe) unsubscribe();
        if (authUnsubscribe) authUnsubscribe();
        notificationStore.stopPolling();
      };
    });
    
    function toggleDropdown() {
      showDropdown = !showDropdown;
    }
    
    async function markAsRead(id) {
      await notificationStore.markAsRead(id);
    }
    
    function handleClickOutside(event) {
      if (showDropdown && !event.target.closest('.notification-dropdown')) {
        showDropdown = false;
      }
    }
  </script>
  
  <svelte:window on:click={handleClickOutside} />
  
  <div class="relative notification-dropdown">
    <button
      type="button"
      class="relative p-1 text-gray-400 hover:text-gray-500"
      on:click={toggleDropdown}
    >
      <span class="sr-only">View notifications</span>
      <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      
      {#if $unreadCount > 0}
        <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white"></span>
      {/if}
    </button>
    
    {#if showDropdown}
      <div class="absolute right-0 z-50 mt-2 w-80 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5">
        <div class="px-4 py-2 border-b border-gray-200">
          <p class="text-sm font-semibold text-gray-900">Notifications</p>
        </div>
        
        {#if notifications.length > 0}
          <div class="max-h-96 overflow-y-auto">
            {#each notifications as notification}
              <button
                class="w-full px-4 py-3 hover:bg-gray-50 text-left {notification.is_read ? 'opacity-60' : ''}"
                on:click={() => markAsRead(notification.id)}
              >
                <p class="text-sm font-medium text-gray-900">{notification.title}</p>
                <p class="text-sm text-gray-500">{notification.message}</p>
                <p class="text-xs text-gray-400 mt-1">
                  {formatRelativeTime(notification.created_at)}
                </p>
              </button>
            {/each}
          </div>
          
          <div class="px-4 py-2 border-t border-gray-200">
            <a href="/notifications" class="text-sm text-indigo-600 hover:text-indigo-500">
              View all notifications
            </a>
          </div>
        {:else}
          <div class="px-4 py-6 text-center text-sm text-gray-500">
            No notifications
          </div>
        {/if}
      </div>
    {/if}
  </div>