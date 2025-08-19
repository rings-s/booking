// src/lib/api/clients.js
import { browser } from '$app/environment';
import { goto } from '$app/navigation';
import { PUBLIC_API_URL } from '$env/static/public';
import toast from 'svelte-french-toast';

const API_URL = PUBLIC_API_URL || 'http://localhost:8000/api';

class APIClient {
  constructor() {
    this.baseURL = API_URL;
    this.fetch = null; // Will be set by SvelteKit load functions
  }

  // Set the fetch function to use (SvelteKit's fetch or window.fetch)
  setFetch(fetchFunction) {
    this.fetch = fetchFunction;
  }

  // Get the appropriate fetch function
  getFetch() {
    return this.fetch || fetch;
  }

  getAuthToken() {
    if (!browser) return null;
    return localStorage.getItem('access_token');
  }

  setAuthTokens(access, refresh) {
    if (!browser) return;
    if (access) localStorage.setItem('access_token', access);
    if (refresh) localStorage.setItem('refresh_token', refresh);
  }

  clearAuthTokens() {
    if (!browser) return;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  async refreshAccessToken() {
    const refreshToken = browser ? localStorage.getItem('refresh_token') : null;
    if (!refreshToken) return null;

    try {
      const response = await this.getFetch()(`${this.baseURL}/accounts/token/refresh/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh: refreshToken })
      });

      if (response.ok) {
        const data = await response.json();
        if (browser) {
          localStorage.setItem('access_token', data.access);
        }
        return data.access;
      }
      return null;
    } catch (error) {
      console.error('Token refresh failed:', error);
      return null;
    }
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const token = this.getAuthToken();

    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    };

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
      config.body = JSON.stringify(options.body);
    }

    try {
      let response = await this.getFetch()(url, config);

      // Handle 401 and retry with refreshed token
      if (response.status === 401 && browser) {
        const newToken = await this.refreshAccessToken();
        if (newToken) {
          config.headers.Authorization = `Bearer ${newToken}`;
          response = await this.getFetch()(url, config);
        } else {
          this.clearAuthTokens();
          if (browser) {
            toast.error('Your session has expired. Please sign in again.');
            goto('/auth/login');
          }
          throw new Error('Authentication required');
        }
      }

      // Handle response
      const contentType = response.headers.get('content-type');
      let data = null;

      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else if (response.ok) {
        data = await response.text();
      }

      if (!response.ok) {
        throw {
          status: response.status,
          statusText: response.statusText,
          data
        };
      }

      return { data, error: null };
    } catch (error) {
      return { data: null, error: this.handleError(error) };
    }
  }

  handleError(error) {
    // Enhanced error handling with better user messages
    let errorMessage = 'An unexpected error occurred';
    let errorType = 'unknown';
    
    if (error.status) {
      errorType = this.getErrorType(error.status);
      
      switch (error.status) {
        case 400:
          errorMessage = 'Invalid request. Please check your input.';
          break;
        case 401:
          errorMessage = 'You need to sign in to access this resource.';
          break;
        case 403:
          errorMessage = 'You do not have permission to perform this action.';
          break;
        case 404:
          errorMessage = 'The requested resource was not found.';
          break;
        case 422:
          errorMessage = 'Please check your input and try again.';
          break;
        case 429:
          errorMessage = 'Too many requests. Please wait a moment and try again.';
          break;
        case 500:
          errorMessage = 'Server error. Please try again later.';
          break;
        case 502:
        case 503:
        case 504:
          errorMessage = 'Service temporarily unavailable. Please try again later.';
          break;
        default:
          errorMessage = `Request failed (${error.status}). Please try again.`;
      }
    }
    
    if (error.data) {
      if (typeof error.data === 'string') {
        errorMessage = error.data;
      } else if (error.data.detail) {
        errorMessage = error.data.detail;
      } else if (error.data.message) {
        errorMessage = error.data.message;
      } else if (error.data.error) {
        errorMessage = error.data.error;
      } else if (error.data.non_field_errors) {
        errorMessage = Array.isArray(error.data.non_field_errors) 
          ? error.data.non_field_errors.join(' ')
          : error.data.non_field_errors;
      } else {
        // Handle field-specific errors
        const fieldErrors = this.extractFieldErrors(error.data);
        if (fieldErrors.length > 0) {
          errorMessage = fieldErrors.join(' ');
        }
      }
    }
    
    return errorMessage;
  }
  
  getErrorType(status) {
    if (status >= 400 && status < 500) return 'client';
    if (status >= 500) return 'server';
    return 'unknown';
  }
  
  extractFieldErrors(data) {
    const errors = [];
    
    for (const [field, messages] of Object.entries(data)) {
      if (Array.isArray(messages)) {
        const fieldName = field === 'non_field_errors' ? '' : `${field}: `;
        errors.push(fieldName + messages.join(', '));
      } else if (typeof messages === 'string') {
        const fieldName = field === 'non_field_errors' ? '' : `${field}: `;
        errors.push(fieldName + messages);
      }
    }
    
    return errors;
  }

  // HTTP method shortcuts
  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    return this.request(url, { method: 'GET' });
  }

  async post(endpoint, body) {
    return this.request(endpoint, { method: 'POST', body });
  }

  async put(endpoint, body) {
    return this.request(endpoint, { method: 'PUT', body });
  }

  async patch(endpoint, body) {
    return this.request(endpoint, { method: 'PATCH', body });
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

export const apiClient = new APIClient();

// Factory function to create API client with SvelteKit fetch
export function createAPIClient(fetch) {
  const client = new APIClient();
  client.setFetch(fetch);
  return client;
}

export default apiClient;