// src/lib/api/auth.js
import apiClient, { createAPIClient } from './clients';
import { browser } from '$app/environment';

export const authAPI = {
  async register(userData) {
    const { data, error } = await apiClient.post('/accounts/register/', userData);
    if (data) {
      apiClient.setAuthTokens(data.access, data.refresh);
    }
    return { data, error };
  },

  async login(credentials) {
    const { data, error } = await apiClient.post('/accounts/login/', credentials);
    if (data) {
      apiClient.setAuthTokens(data.access, data.refresh);
    }
    return { data, error };
  },

  async googleLogin(accessToken) {
    const { data, error } = await apiClient.post('/accounts/google-login/', {
      access_token: accessToken
    });
    if (data) {
      apiClient.setAuthTokens(data.access, data.refresh);
    }
    return { data, error };
  },

  async googleCallback(authCode) {
    const { data, error } = await apiClient.post('/accounts/google-callback/', {
      code: authCode
    });
    if (data) {
      apiClient.setAuthTokens(data.access, data.refresh);
    }
    return { data, error };
  },

  async logout() {
    apiClient.clearAuthTokens();
    return { data: { message: 'Logged out successfully' }, error: null };
  },

  async getCurrentUser() {
    return apiClient.get('/accounts/users/me/');
  },

  async changePassword(passwordData) {
    return apiClient.post('/accounts/users/change_password/', passwordData);
  },

  async refreshToken(refreshToken) {
    return apiClient.post('/accounts/token/refresh/', { refresh: refreshToken });
  }
};

// Server-side safe function to get current user with SvelteKit fetch
export async function getCurrentUserSSR(fetch) {
  if (!browser) return { data: null, error: null };
  
  const token = localStorage.getItem('access_token');
  if (!token) return { data: null, error: null };
  
  const client = createAPIClient(fetch);
  return client.get('/accounts/users/me/');
}