// src/lib/api/customers.js
import apiClient from './client';

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
    const params = { period };
    if (businessId) {
      params.business = businessId;
    }
    return apiClient.get('/customers/chart-data/', params);
  },

  async getTopCustomers(businessId, limit = 10) {
    const params = { limit };
    if (businessId) {
      params.business = businessId;
    }
    return apiClient.get('/customers/top/', params);
  },

  async getCustomerRetention(businessId, period = 'month') {
    const params = { period };
    if (businessId) {
      params.business = businessId;
    }
    return apiClient.get('/customers/retention/', params);
  },

  async getCustomerSegments(businessId) {
    const params = {};
    if (businessId) {
      params.business = businessId;
    }
    return apiClient.get('/customers/segments/', params);
  }
};