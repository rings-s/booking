// src/lib/api/services.js
import apiClient from './client';

export const serviceAPI = {
  async list(params = {}) {
    return apiClient.get('/services/', params);
  },

  async get(id) {
    return apiClient.get(`/services/${id}/`);
  },

  async create(serviceData) {
    return apiClient.post('/services/', serviceData);
  },

  async update(id, serviceData) {
    return apiClient.patch(`/services/${id}/`, serviceData);
  },

  async delete(id) {
    return apiClient.delete(`/services/${id}/`);
  },

  async getByBusiness(businessId, params = {}) {
    return apiClient.get('/services/', { ...params, business: businessId });
  },

  async getByPriceRange(minPrice, maxPrice) {
    return apiClient.get('/services/', { 
      min_price: minPrice, 
      max_price: maxPrice 
    });
  },

  async toggleActive(id) {
    return apiClient.patch(`/services/${id}/`, { is_active: true });
  },

  async bulkUpdate(updates) {
    return apiClient.post('/services/bulk-update/', { updates });
  },

  async updateOrder(updates) {
    return apiClient.post('/services/update-order/', { updates });
  }
};