// src/lib/api/bookings.js
import apiClient from './client';

export const bookingAPI = {
  async list(params = {}) {
    return apiClient.get('/bookings/', params);
  },

  async get(id) {
    return apiClient.get(`/bookings/${id}/`);
  },

  async getById(id) {
    return apiClient.get(`/bookings/${id}/`);
  },

  async create(bookingData) {
    return apiClient.post('/bookings/', bookingData);
  },

  async update(id, bookingData) {
    return apiClient.patch(`/bookings/${id}/`, bookingData);
  },

  async delete(id) {
    return apiClient.delete(`/bookings/${id}/`);
  },

  async confirm(id) {
    return apiClient.post(`/bookings/${id}/confirm/`);
  },

  async cancel(id) {
    return apiClient.post(`/bookings/${id}/cancel/`);
  },

  async complete(id) {
    return apiClient.post(`/bookings/${id}/complete/`);
  },

  async markNoShow(id) {
    return apiClient.post(`/bookings/${id}/mark-no-show/`);
  },

  async getUpcoming() {
    return apiClient.get('/bookings/upcoming/');
  },

  async getHistory() {
    return apiClient.get('/bookings/history/');
  },

  async getByBusiness(businessId, params = {}) {
    return apiClient.get('/bookings/', { ...params, business: businessId });
  },

  async getByDateRange(startDate, endDate) {
    return apiClient.get('/bookings/', { 
      start_date: startDate, 
      end_date: endDate 
    });
  },

  async updateStatus(id, status) {
    return apiClient.patch(`/bookings/${id}/`, { status });
  },

  async reschedule(id, rescheduleData) {
    return apiClient.post(`/bookings/${id}/reschedule/`, rescheduleData);
  },

  async getAvailableSlots(params) {
    return apiClient.get('/bookings/available-slots/', params);
  },

  // Dashboard methods
  async getChartData(businessId, period = 'month') {
    const params = { period };
    if (businessId) {
      params.business = businessId;
    }
    return apiClient.get('/bookings/chart-data/', params);
  },

  async getStatusBreakdown(businessId, period = 'month') {
    const params = { period };
    if (businessId) {
      params.business = businessId;
    }
    return apiClient.get('/bookings/status-breakdown/', params);
  },

  async getBookingTrends(businessId, period = 'month') {
    const params = { period };
    if (businessId) {
      params.business = businessId;
    }
    return apiClient.get('/bookings/trends/', params);
  },

  async getBookingHeatmap(businessId, period = 'month') {
    const params = { period };
    if (businessId) {
      params.business = businessId;
    }
    return apiClient.get('/bookings/heatmap/', params);
  },

  async getBookingInsights(businessId, period = 'month') {
    const params = { period };
    if (businessId) {
      params.business = businessId;
    }
    return apiClient.get('/bookings/insights/', params);
  }
};