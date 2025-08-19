// src/lib/api/subscriptions.js
import apiClient from './clients.js';

export const subscriptionAPI = {
  async getPlans() {
    return apiClient.get('/accounts/plans/');
  },

  async getCurrentSubscription() {
    return apiClient.get('/accounts/subscriptions/');
  },

  async createSubscription(planId, paymentMethodId) {
    return apiClient.post('/accounts/subscriptions/', {
      plan_id: planId,
      payment_method_id: paymentMethodId
    });
  },

  async updateSubscription(subscriptionId, planId) {
    return apiClient.patch(`/accounts/subscriptions/${subscriptionId}/`, {
      plan_id: planId
    });
  },

  async cancelSubscription(subscriptionId) {
    return apiClient.post(`/accounts/subscriptions/${subscriptionId}/cancel/`);
  },

  async resumeSubscription(subscriptionId) {
    return apiClient.post(`/accounts/subscriptions/${subscriptionId}/resume/`);
  },

  async getInvoices() {
    return apiClient.get('/accounts/subscriptions/invoices/');
  },

  async downloadInvoice(invoiceId) {
    // Backend doesn't provide download functionality yet - return mock response
    return { data: { message: 'Download functionality not implemented yet' }, error: null };
  },

  async updatePaymentMethod(paymentMethodId) {
    // Backend doesn't have this endpoint yet - use upgrade endpoint for now
    return apiClient.post('/accounts/subscriptions/upgrade/', {
      payment_method_id: paymentMethodId
    });
  },

  async getUsage() {
    return apiClient.get('/accounts/subscriptions/usage/');
  }
};