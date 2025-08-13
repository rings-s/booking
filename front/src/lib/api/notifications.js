// src/lib/api/notifications.js
import apiClient from './client';

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
    return apiClient.post('/notifications/settings/', settings);
  },

  async getSettings() {
    return apiClient.get('/notifications/settings/');
  },

  async subscribe(subscription) {
    return apiClient.post('/notifications/subscribe/', subscription);
  },

  async unsubscribe() {
    return apiClient.post('/notifications/unsubscribe/');
  },

  async sendBookingReminder(bookingId) {
    return apiClient.post(`/bookings/${bookingId}/send-reminder/`);
  }
};