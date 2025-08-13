// src/lib/api/reviews.js
import apiClient from './client';

export const reviewAPI = {
  async list(params = {}) {
    return apiClient.get('/reviews/', params);
  },

  async get(id) {
    return apiClient.get(`/reviews/${id}/`);
  },

  async create(reviewData) {
    return apiClient.post('/reviews/', reviewData);
  },

  async update(id, reviewData) {
    return apiClient.patch(`/reviews/${id}/`, reviewData);
  },

  async delete(id) {
    return apiClient.delete(`/reviews/${id}/`);
  },

  async getByBusiness(businessId, params = {}) {
    return apiClient.get('/reviews/', { ...params, business: businessId });
  },

  async getByCustomer(customerId) {
    return apiClient.get('/reviews/', { customer: customerId });
  },

  async respond(id, response) {
    return apiClient.post(`/reviews/${id}/respond/`, { response });
  },

  async markFeatured(id) {
    return apiClient.post(`/reviews/${id}/mark-featured/`);
  },

  async getStats(businessId) {
    return apiClient.get(`/reviews/stats/`, { business: businessId });
  }
};