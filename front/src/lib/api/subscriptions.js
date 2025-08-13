// src/lib/api/subscriptions.js
import apiClient from './client.js';

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
    return apiClient.get(`/accounts/subscriptions/invoices/${invoiceId}/download/`);
  },

  async updatePaymentMethod(paymentMethodId) {
    return apiClient.post('/accounts/subscriptions/update-payment-method/', {
      payment_method_id: paymentMethodId
    });
  },

  async getUsage() {
    return apiClient.get('/accounts/subscriptions/usage/');
  }
};