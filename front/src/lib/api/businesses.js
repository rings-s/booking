// src/lib/api/businesses.js
import apiClient from './client';

export const businessAPI = {
  async list(params = {}) {
    return apiClient.get('/businesses/', params);
  },

  async search(params = {}) {
    return apiClient.get('/businesses/search/', params);
  },

  async getFeatured() {
    return apiClient.get('/businesses/featured/');
  },

  async get(slug) {
    return apiClient.get(`/businesses/${slug}/`);
  },

  async create(businessData) {
    return apiClient.post('/businesses/', businessData);
  },

  async update(slug, businessData) {
    return apiClient.patch(`/businesses/${slug}/`, businessData);
  },

  async delete(slug) {
    return apiClient.delete(`/businesses/${slug}/`);
  },

  async getDashboard(slug) {
    return apiClient.get(`/businesses/${slug}/dashboard/`);
  },

  async getAnalyticsChart(slug, type = 'bookings', period = 30) {
    return apiClient.get(`/businesses/${slug}/analytics-chart/`, { type, period });
  },

  async getAvailableSlots(slug, serviceId, date) {
    return apiClient.get(`/businesses/${slug}/available-slots/`, { 
      service: serviceId, 
      date 
    });
  },

  async getAvailableDates(slug, serviceId, daysAhead = 90) {
    return apiClient.get(`/businesses/${slug}/available-dates/`, { 
      service: serviceId, 
      days_ahead: daysAhead 
    });
  },

  async updateHours(slug, hoursData) {
    return apiClient.post(`/businesses/${slug}/update-hours/`, { hours: hoursData });
  },

  async getRevenueReport(slug, period = 'month') {
    return apiClient.get(`/businesses/${slug}/revenue-report/`, { period });
  },

  async uploadLogo(slug, file) {
    const formData = new FormData();
    formData.append('logo', file);
    
    return apiClient.request(`/businesses/${slug}/`, {
      method: 'PATCH',
      body: formData,
      headers: {} // Let browser set content-type for FormData
    });
  },

  async getServices(businessSlug) {
    return apiClient.get(`/businesses/${businessSlug}/services/`);
  },

  async addFavorite(businessId) {
    return apiClient.post('/customers/me/add-preferred-business/', { business_id: businessId });
  },

  async removeFavorite(businessId) {
    return apiClient.delete(`/customers/me/preferred-businesses/${businessId}/`);
  },

  async checkSlug(slug) {
    return apiClient.get(`/businesses/check-slug/`, { slug });
  },

  // Dashboard methods
  async getMyBusinesses() {
    return apiClient.get('/businesses/my/');
  },
  
  // Helper method to get business identifier (slug or ID) from business object
  getBusinessIdentifier(business) {
    // Prefer slug for URL-friendly endpoints, fallback to ID
    return business.slug || business.id;
  },
  
  // Helper method to format business data for dashboard
  formatBusinessForDashboard(business) {
    return {
      id: business.id,
      slug: business.slug,
      name: business.name,
      identifier: this.getBusinessIdentifier(business)
    };
  },

  // Fixed to use business slug instead of ID for endpoints that expect slug
  async getStats(businessIdentifier, period = 'month') {
    return apiClient.get(`/businesses/${businessIdentifier}/stats/`, { period });
  },

  async getRevenueData(businessIdentifier, period = 'month') {
    return apiClient.get(`/businesses/${businessIdentifier}/revenue-data/`, { period });
  },

  async getServiceStats(businessIdentifier, period = 'month') {
    return apiClient.get(`/businesses/${businessIdentifier}/service-stats/`, { period });
  },

  async getRecentActivity(businessIdentifier) {
    return apiClient.get(`/businesses/${businessIdentifier}/recent-activity/`);
  },

  // Additional dashboard methods
  async getBySlug(slug) {
    return apiClient.get(`/businesses/${slug}/`);
  },

  async getCustomerAnalytics(businessId, period = 'month') {
    return apiClient.get(`/businesses/${businessId}/customer-analytics/`, { period });
  },

  async getTopCustomers(businessId, period = 'month') {
    return apiClient.get(`/businesses/${businessId}/top-customers/`, { period });
  },

  async getPeakHours(businessId) {
    return apiClient.get(`/businesses/${businessId}/peak-hours/`);
  },

  async exportAnalytics(businessId, period = 'month') {
    return apiClient.get(`/businesses/${businessId}/export-analytics/`, { period });
  },

  // Chart integration methods
  async getChartData(businessId, type = 'revenue', period = 'month') {
    return apiClient.get(`/businesses/${businessId}/chart-data/`, { type, period });
  },

  async getPlotlyChart(businessId, type = 'revenue', period = 'month') {
    return apiClient.get(`/businesses/${businessId}/plotly-chart/`, { type, period });
  },

  // Enhanced analytics methods
  async getPerformanceMetrics(businessId, period = 'month') {
    return apiClient.get(`/businesses/${businessId}/performance/`, { period });
  },

  async getBookingTrends(businessId, period = 'month') {
    return apiClient.get(`/businesses/${businessId}/booking-trends/`, { period });
  },

  async getRevenueTrends(businessIdentifier, period = 'month') {
    return apiClient.get(`/businesses/${businessIdentifier}/revenue-trends/`, { period });
  },
  
  // Alternative method that works with both slug and ID
  async getBusinessData(identifier, endpoint, params = {}) {
    // Try with identifier as-is first
    const url = `/businesses/${identifier}/${endpoint}/`;
    return apiClient.get(url, params);
  }
};