// src/lib/api/customers.js
import apiClient from './clients';

export const customerAPI = {
  async list(params = {}) {
    return apiClient.get('/customers/', params);
  },

  async get(id) {
    return apiClient.get(`/customers/${id}/`);
  },

  async getMe() {
    return apiClient.get('/customers/me/');
  },

  async update(id, customerData) {
    return apiClient.patch(`/customers/${id}/`, customerData);
  },

  async updateMe(customerData) {
    const { data: me } = await this.getMe();
    if (me) {
      return apiClient.patch(`/customers/${me.id}/`, customerData);
    }
    return { error: 'Customer profile not found' };
  },

  async addPreferredBusiness(customerId, businessId) {
    return apiClient.post(`/customers/${customerId}/add-preferred-business/`, {
      business_id: businessId
    });
  },

  async removePreferredBusiness(customerId, businessId) {
    return apiClient.post(`/customers/${customerId}/remove-preferred-business/`, {
      business_id: businessId
    });
  },

  async getBookingHistory(customerId) {
    return apiClient.get(`/customers/${customerId}/booking-history/`);
  },

  async getStats(customerId) {
    return apiClient.get(`/customers/${customerId}/stats/`);
  },

  // Dashboard methods
  async getAnalytics(businessId, period = 'month') {
    const params = { period };
    if (businessId) {
      params.business = businessId;
    }
    return apiClient.get('/customers/analytics/', params);
  },

  async getChartData(businessId, period = 'month') {
    // Backend doesn't have chart-data endpoint yet - return mock response
    return { data: { 
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
      datasets: [{ label: 'New Customers', data: [12, 19, 8, 15, 22] }]
    }, error: null };
  },

  async getTopCustomers(businessId, limit = 10) {
    // Backend doesn't have top customers endpoint yet - return mock response
    return { data: [], error: null };
  },

  async getCustomerRetention(businessId, period = 'month') {
    // Backend doesn't have retention endpoint yet - return mock response
    return { data: { retention_rate: 85.5 }, error: null };
  },

  async getCustomerSegments(businessId) {
    // Backend doesn't have segments endpoint yet - return mock response
    return { data: [], error: null };
  }
};