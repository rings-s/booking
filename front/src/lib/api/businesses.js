// src/lib/api/businesses.js
import apiClient from './clients';

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

  // Dashboard methods - using consistent naming with store
  async dashboard(slug) {
    return apiClient.get(`/businesses/${slug}/dashboard/`);
  },

  async getDashboard(slug) {
    return this.dashboard(slug);
  },

  async analyticsChart(slug, type = 'bookings', period = 30) {
    return apiClient.get(`/businesses/${slug}/analytics-chart/`, { type, period });
  },

  async getAnalyticsChart(slug, type = 'bookings', period = 30) {
    return this.analyticsChart(slug, type, period);
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
    return apiClient.post('/customers/me/remove-preferred-business/', {
      business_id: businessId
    });
  },

  async checkSlug(slug) {
    // Backend doesn't have check-slug endpoint yet - return mock response
    return { data: { available: true }, error: null };
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

  // Dashboard API methods - consistent naming with store
  async stats(businessIdentifier, params = {}) {
    return apiClient.get(`/businesses/${businessIdentifier}/stats/`, params);
  },

  async getStats(businessIdentifier, period = 'month') {
    return this.stats(businessIdentifier, { period });
  },

  async revenueData(businessIdentifier, params = {}) {
    return apiClient.get(`/businesses/${businessIdentifier}/revenue-data/`, params);
  },

  async getRevenueData(businessIdentifier, period = 'month') {
    return this.revenueData(businessIdentifier, { period });
  },

  async serviceStats(businessIdentifier, params = {}) {
    return apiClient.get(`/businesses/${businessIdentifier}/service-stats/`, params);
  },

  async getServiceStats(businessIdentifier, period = 'month') {
    return this.serviceStats(businessIdentifier, { period });
  },

  async recentActivity(businessIdentifier) {
    return apiClient.get(`/businesses/${businessIdentifier}/recent-activity/`);
  },

  async getRecentActivity(businessIdentifier) {
    return this.recentActivity(businessIdentifier);
  },

  // Additional dashboard methods
  async getBySlug(slug) {
    return apiClient.get(`/businesses/${slug}/`);
  },

  async getCustomerAnalytics(businessId, period = 'month') {
    // Backend doesn't have customer-analytics endpoint yet - return mock response
    return { data: { new_customers: 15, returning_customers: 45, retention_rate: 78.5 }, error: null };
  },

  async getTopCustomers(businessId, period = 'month') {
    // Backend doesn't have top-customers endpoint yet - return mock response
    return { data: [], error: null };
  },

  async getPeakHours(businessId) {
    // Backend doesn't have peak-hours endpoint yet - return mock response
    return { data: { peak_hours: ['10:00', '14:00', '16:00'] }, error: null };
  },

  async exportAnalytics(businessId, period = 'month') {
    // Backend doesn't have export-analytics endpoint yet - return mock response
    return { data: { download_url: null, message: 'Export functionality not implemented yet' }, error: null };
  },

  // Chart integration methods
  async getChartData(businessId, type = 'revenue', period = 'month') {
    // Backend doesn't have chart-data endpoint yet - return mock response
    return { data: { labels: [], datasets: [] }, error: null };
  },

  async getPlotlyChart(businessId, type = 'revenue', period = 'month') {
    // Backend doesn't have plotly-chart endpoint yet - return mock response
    return { data: { chart: '<div>Chart not available</div>' }, error: null };
  },

  // Enhanced analytics methods
  async getPerformanceMetrics(businessId, period = 'month') {
    // Backend doesn't have performance endpoint yet - return mock response
    return { data: { occupancy_rate: 82.3, avg_booking_value: 125.50 }, error: null };
  },

  async getBookingTrends(businessId, period = 'month') {
    // Backend doesn't have booking-trends endpoint yet - return mock response
    return { data: { trend: 'up', change_percentage: 15.2 }, error: null };
  },

  async getRevenueTrends(businessIdentifier, period = 'month') {
    // Backend doesn't have revenue-trends endpoint yet - return mock response
    return { data: { trend: 'up', change_percentage: 8.7 }, error: null };
  },
  
  // Alternative method that works with both slug and ID
  async getBusinessData(identifier, endpoint, params = {}) {
    // Try with identifier as-is first
    const url = `/businesses/${identifier}/${endpoint}/`;
    return apiClient.get(url, params);
  }
};