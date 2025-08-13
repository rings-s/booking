// src/lib/stores/notification.js
import { writable, derived } from 'svelte/store';
import { notificationAPI } from '$lib/api/notifications';
import { browser } from '$app/environment';
import toast from 'svelte-french-toast';

function createNotificationStore() {
  const { subscribe, set, update } = writable({
    notifications: [],
    unreadCount: 0,
    loading: false,
    error: null
  });

  let pollInterval = null;

  return {
    subscribe,

    async loadNotifications() {
      update(state => ({ ...state, loading: true, error: null }));
      
      const { data, error } = await notificationAPI.list();
      
      if (error) {
        update(state => ({ ...state, loading: false, error }));
      } else {
        const notifications = data.results || data || [];
        const unreadCount = notifications.filter(n => !n.is_read).length;
        
        update(state => ({
          ...state,
          notifications,
          unreadCount,
          loading: false
        }));
      }
    },

    async loadUnreadCount() {
      try {
        const { data, error } = await notificationAPI.getUnreadCount();
        
        if (!error && data) {
          update(state => ({
            ...state,
            unreadCount: data.unread_count || 0,
            error: null
          }));
        } else if (error) {
          // Stop polling on error to prevent repeated 404s
          this.stopPolling();
          update(state => ({
            ...state,
            error: error
          }));
        }
      } catch (err) {
        // Stop polling on any exception
        this.stopPolling();
        update(state => ({
          ...state,
          error: err.message || 'Failed to load notifications'
        }));
      }
    },

    async markAsRead(id) {
      const { data, error } = await notificationAPI.markRead(id);
      
      if (!error) {
        update(state => ({
          ...state,
          notifications: state.notifications.map(n =>
            n.id === id ? { ...n, is_read: true } : n
          ),
          unreadCount: Math.max(0, state.unreadCount - 1)
        }));
      }
    },

    async markAllAsRead() {
      const { data, error } = await notificationAPI.markAllRead();
      
      if (!error) {
        update(state => ({
          ...state,
          notifications: state.notifications.map(n => ({ ...n, is_read: true })),
          unreadCount: 0
        }));
        toast.success('All notifications marked as read');
      }
    },

    async clearAll() {
      const { data, error } = await notificationAPI.clearAll();
      
      if (!error) {
        update(state => ({
          ...state,
          notifications: state.notifications.filter(n => !n.is_read)
        }));
        toast.success('Cleared all read notifications');
      }
    },

    startPolling(interval = 30000) {
      if (!browser) return;
      
      this.stopPolling();
      pollInterval = setInterval(() => {
        this.loadUnreadCount();
      }, interval);
    },

    stopPolling() {
      if (pollInterval) {
        clearInterval(pollInterval);
        pollInterval = null;
      }
    },

    showNotification(notification) {
      if (!browser) return;
      
      // Show browser notification if permitted
      if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(notification.title, {
          body: notification.message,
          icon: '/favicon.png'
        });
      }
      
      // Show toast notification
      toast(notification.message, {
        icon: '🔔'
      });
      
      // Add to store
      update(state => ({
        ...state,
        notifications: [notification, ...state.notifications],
        unreadCount: state.unreadCount + 1
      }));
    },

    async requestPermission() {
      if (!browser || !('Notification' in window)) return false;
      
      if (Notification.permission === 'default') {
        const permission = await Notification.requestPermission();
        return permission === 'granted';
      }
      
      return Notification.permission === 'granted';
    },

    reset() {
      this.stopPolling();
      set({
        notifications: [],
        unreadCount: 0,
        loading: false,
        error: null
      });
    }
  };
}

export const notificationStore = createNotificationStore();

// Derived stores
export const notifications = derived(notificationStore, $store => $store.notifications);
export const unreadCount = derived(notificationStore, $store => $store.unreadCount);
export const hasUnread = derived(notificationStore, $store => $store.unreadCount > 0);