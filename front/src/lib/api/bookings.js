// src/lib/api/bookings.js
import apiClient from './clients';

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
    // Backend doesn't have reschedule endpoint yet - use update instead
    return apiClient.patch(`/bookings/${id}/`, {
      booking_date: rescheduleData.date,
      start_time: rescheduleData.start_time,
      end_time: rescheduleData.end_time
    });
  },

  async getAvailableSlots(params) {
    // Backend doesn't have global available-slots - use business-specific endpoint
    if (params.business_slug) {
      return apiClient.get(`/businesses/${params.business_slug}/available-slots/`, params);
    }
    return { data: [], error: 'Business slug required for available slots' };
  },

  // Dashboard methods - consistent naming with store
  async chartData(params = {}) {
    return apiClient.get('/bookings/chart-data/', params);
  },

  async getChartData(businessId, period = 'month') {
    const params = { period };
    if (businessId) {
      params.business = businessId;
    }
    return this.chartData(params);
  },

  async getStatusBreakdown(businessId, period = 'month') {
    // Backend doesn't have status-breakdown endpoint yet - return mock response
    return { data: {
      confirmed: 45,
      pending: 12,
      cancelled: 8,
      completed: 156,
      no_show: 3
    }, error: null };
  },

  async getBookingTrends(businessId, period = 'month') {
    // Backend doesn't have trends endpoint yet - return mock response
    return { data: {
      labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
      data: [25, 32, 28, 41]
    }, error: null };
  },

  async getBookingHeatmap(businessId, period = 'month') {
    // Backend doesn't have heatmap endpoint yet - return mock response
    return { data: {
      hours: Array.from({length: 24}, (_, i) => i),
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      data: Array.from({length: 7}, () => Array.from({length: 24}, () => Math.floor(Math.random() * 10)))
    }, error: null };
  },

  async getBookingInsights(businessId, period = 'month') {
    // Backend doesn't have insights endpoint yet - return mock response
    return { data: {
      peak_hours: ['10:00-12:00', '14:00-16:00'],
      popular_services: [],
      avg_booking_value: 85.50,
      customer_satisfaction: 4.8
    }, error: null };
  }
};