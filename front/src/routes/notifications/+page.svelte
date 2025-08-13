<!-- src/routes/notifications/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import { notificationAPI } from '$lib/api/notifications';
    import { notificationStore } from '$lib/stores/notification';
    import Avatar from '$lib/components/common/Avatar.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import toast from 'svelte-french-toast';
    import { formatRelativeTime } from '$lib/utils/formatters';
    
    let notifications = [];
    let loading = true;
    let filterType = '';
    let filterRead = '';
    let selectedNotification = null;
    let showDetailsModal = false;
    let markingAsRead = false;
    
    const typeOptions = [
      { value: '', label: 'All Types' },
      { value: 'booking', label: 'Bookings' },
      { value: 'payment', label: 'Payments' },
      { value: 'review', label: 'Reviews' },
      { value: 'reminder', label: 'Reminders' },
      { value: 'system', label: 'System' }
    ];
    
    const readOptions = [
      { value: '', label: 'All' },
      { value: 'unread', label: 'Unread' },
      { value: 'read', label: 'Read' }
    ];
    
    onMount(async () => {
      await loadNotifications();
    });
    
    async function loadNotifications() {
      loading = true;
      
      const params = {
        type: filterType,
        read: filterRead === 'read' ? true : filterRead === 'unread' ? false : undefined
      };
      
      const { data, error } = await notificationAPI.getAll(params);
      
      if (data) {
        notifications = data;
        // Update unread count in store
        const unreadCount = data.filter(n => !n.is_read).length;
        notificationStore.setUnreadCount(unreadCount);
      }
      
      loading = false;
    }
    
    async function markAsRead(notificationId) {
      const { data, error } = await notificationAPI.markAsRead(notificationId);
      
      if (data) {
        const index = notifications.findIndex(n => n.id === notificationId);
        notifications[index].is_read = true;
        notificationStore.decrementUnread();
      }
    }
    
    async function markAllAsRead() {
      markingAsRead = true;
      const { data, error } = await notificationAPI.markAllAsRead();
      
      if (data) {
        notifications = notifications.map(n => ({ ...n, is_read: true }));
        notificationStore.setUnreadCount(0);
        toast.success('All notifications marked as read');
      }
      
      markingAsRead = false;
    }
    
    async function deleteNotification(notificationId) {
      const { data, error } = await notificationAPI.delete(notificationId);
      
      if (data) {
        notifications = notifications.filter(n => n.id !== notificationId);
        toast.success('Notification deleted');
        showDetailsModal = false;
      }
    }
    
    async function deleteAllRead() {
      if (!confirm('Are you sure you want to delete all read notifications?')) return;
      
      const { data, error } = await notificationAPI.deleteAllRead();
      
      if (data) {
        notifications = notifications.filter(n => !n.is_read);
        toast.success('Read notifications deleted');
      }
    }
    
    function viewDetails(notification) {
      selectedNotification = notification;
      showDetailsModal = true;
      
      if (!notification.is_read) {
        markAsRead(notification.id);
      }
    }
    
    function getNotificationIcon(type) {
      switch (type) {
        case 'booking':
          return 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z';
        case 'payment':
          return 'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z';
        case 'review':
          return 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z';
        case 'reminder':
          return 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9';
        default:
          return 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z';
      }
    }
    
    function getNotificationColor(type) {
      switch (type) {
        case 'booking': return 'bg-blue-100 text-blue-600';
        case 'payment': return 'bg-green-100 text-green-600';
        case 'review': return 'bg-yellow-100 text-yellow-600';
        case 'reminder': return 'bg-purple-100 text-purple-600';
        default: return 'bg-gray-100 text-gray-600';
      }
    }
    
    // Group notifications by date
    $: groupedNotifications = notifications.reduce((groups, notification) => {
      const date = new Date(notification.created_at).toDateString();
      if (!groups[date]) {
        groups[date] = [];
      }
      groups[date].push(notification);
      return groups;
    }, {});
    
    $: unreadCount = notifications.filter(n => !n.is_read).length;
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Notifications</h1>
            <p class="mt-1 text-sm text-gray-600">
              {unreadCount > 0 ? `You have ${unreadCount} unread notifications` : 'All caught up!'}
            </p>
          </div>
          
          <div class="flex items-center space-x-3">
            {#if unreadCount > 0}
              <Button
                variant="outline"
                on:click={markAllAsRead}
                loading={markingAsRead}
              >
                Mark All as Read
              </Button>
            {/if}
            
            {#if notifications.some(n => n.is_read)}
              <Button
                variant="outline"
                on:click={deleteAllRead}
              >
                Clear Read
              </Button>
            {/if}
          </div>
        </div>
      </div>
    </div>
    
    <!-- Filters -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <Card>
        <div class="flex flex-wrap items-center gap-4">
          <select
            bind:value={filterType}
            on:change={loadNotifications}
            class="rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm"
          >
            {#each typeOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
          
          <select
            bind:value={filterRead}
            on:change={loadNotifications}
            class="rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm"
          >
            {#each readOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>
      </Card>
    </div>
    
    <!-- Notifications List -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
      {#if loading}
        <div class="flex justify-center py-12">
          <Spinner size="lg">Loading notifications...</Spinner>
        </div>
      {:else if notifications.length === 0}
        <Card>
          <div class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <h3 class="mt-2 text-lg font-medium text-gray-900">No notifications</h3>
            <p class="mt-1 text-sm text-gray-500">
              {filterType || filterRead ? 'No notifications match your filters' : "You're all caught up!"}
            </p>
          </div>
        </Card>
      {:else}
        <div class="space-y-6">
          {#each Object.entries(groupedNotifications) as [date, dateNotifications]}
            <div>
              <h3 class="text-sm font-medium text-gray-500 mb-3">
                {date === new Date().toDateString() 
                  ? 'Today' 
                  : date === new Date(Date.now() - 86400000).toDateString()
                  ? 'Yesterday'
                  : date}
              </h3>
              
              <Card>
                <div class="divide-y divide-gray-200">
                  {#each dateNotifications as notification}
                    <div
                      class="p-4 hover:bg-gray-50 cursor-pointer transition-colors
                             {!notification.is_read ? 'bg-indigo-50' : ''}"
                      on:click={() => viewDetails(notification)}
                    >
                      <div class="flex items-start space-x-3">
                        <div class="flex-shrink-0">
                          <div class="p-2 rounded-lg {getNotificationColor(notification.type)}">
                            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                    d={getNotificationIcon(notification.type)} />
                            </svg>
                          </div>
                        </div>
                        
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between">
                            <div>
                              <p class="text-sm font-medium text-gray-900">
                                {notification.title}
                              </p>
                              <p class="text-sm text-gray-600 mt-1">
                                {notification.message}
                              </p>
                            </div>
                            
                            {#if !notification.is_read}
                              <span class="flex-shrink-0 w-2 h-2 bg-indigo-600 rounded-full"></span>
                            {/if}
                          </div>
                          
                          <p class="text-xs text-gray-500 mt-2">
                            {formatRelativeTime(notification.created_at)}
                          </p>
                        </div>
                      </div>
                    </div>
                  {/each}
                </div>
              </Card>
            </div>
          {/each}
        </div>
      {/if}
    </div>
    
    <!-- Notification Details Modal -->
    <Modal bind:open={showDetailsModal} title="Notification Details" size="md">
      {#if selectedNotification}
        <div class="space-y-4">
          <div class="flex items-center space-x-3">
            <div class="p-2 rounded-lg {getNotificationColor(selectedNotification.type)}">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d={getNotificationIcon(selectedNotification.type)} />
              </svg>
            </div>
            
            <div>
              <h3 class="text-lg font-medium text-gray-900">
                {selectedNotification.title}
              </h3>
              <p class="text-sm text-gray-500">
                {new Date(selectedNotification.created_at).toLocaleString()}
              </p>
            </div>
          </div>
          
          <div class="prose prose-sm max-w-none">
            <p>{selectedNotification.message}</p>
          </div>
          
          {#if selectedNotification.action_url}
            <Button fullWidth href={selectedNotification.action_url}>
              {selectedNotification.action_text || 'View Details'}
            </Button>
          {/if}
        </div>
      {/if}
      
      <div slot="footer" class="flex justify-between">
        <Button
          variant="outline"
          on:click={() => deleteNotification(selectedNotification.id)}
        >
          Delete
        </Button>
        
        <Button on:click={() => showDetailsModal = false}>
          Close
        </Button>
      </div>
    </Modal>
  </div>