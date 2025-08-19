// src/lib/api/notifications.js
import apiClient from './clients';

export const notificationAPI = {
  async list(params = {}) {
    return apiClient.get('/notifications/', params);
  },

  async get(id) {
    return apiClient.get(`/notifications/${id}/`);
  },

  async markRead(id) {
    return apiClient.post(`/notifications/${id}/mark-read/`);
  },

  async markAllRead() {
    return apiClient.post('/notifications/mark-all-read/');
  },

  async getUnreadCount() {
    return apiClient.get('/notifications/unread-count/');
  },

  async clearAll() {
    return apiClient.delete('/notifications/clear-all/');
  },

  async updateSettings(settings) {
    // Backend doesn't have settings endpoint yet - return mock response
    return { data: { message: 'Notification settings will be implemented in a future update' }, error: null };
  },

  async getSettings() {
    // Backend doesn't have settings endpoint yet - return mock response
    return { data: { 
      email_notifications: true, 
      push_notifications: true,
      reminder_notifications: true 
    }, error: null };
  },

  async subscribe(subscription) {
    // Backend doesn't have subscribe endpoint yet - return mock response
    return { data: { message: 'Notification subscription will be implemented in a future update' }, error: null };
  },

  async unsubscribe() {
    // Backend doesn't have unsubscribe endpoint yet - return mock response
    return { data: { message: 'Notification unsubscribe will be implemented in a future update' }, error: null };
  },

  async sendBookingReminder(bookingId) {
    // Backend doesn't have send-reminder endpoint yet - return mock response
    return { data: { message: 'Booking reminder functionality will be implemented in a future update' }, error: null };
  }
};