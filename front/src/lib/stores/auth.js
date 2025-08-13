// src/lib/stores/auth.js
import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';
import { authAPI } from '$lib/api/auth';
import { goto } from '$app/navigation';

function createAuthStore() {
  const { subscribe, set, update } = writable({
    user: null,
    isAuthenticated: false,
    isLoading: true
  });

  return {
    subscribe,
    
    async init() {
      if (!browser) return;
      
      const token = localStorage.getItem('access_token');
      if (token) {
        const { data, error } = await authAPI.getCurrentUser();
        if (data) {
          set({
            user: data,
            isAuthenticated: true,
            isLoading: false
          });
        } else {
          this.logout();
        }
      } else {
        set({
          user: null,
          isAuthenticated: false,
          isLoading: false
        });
      }
    },

    async login(credentials) {
      const { data, error } = await authAPI.login(credentials);
      if (data) {
        set({
          user: data.user,
          isAuthenticated: true,
          isLoading: false
        });
        goto('/dashboard');
      }
      return { data, error };
    },

    async register(userData) {
      const { data, error } = await authAPI.register(userData);
      if (data) {
        set({
          user: data.user,
          isAuthenticated: true,
          isLoading: false
        });
        goto('/dashboard');
      }
      return { data, error };
    },

    async logout() {
      await authAPI.logout();
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false
      });
      goto('/');
    },

    setUser(user) {
      set({
        user,
        isAuthenticated: !!user,
        isLoading: false
      });
    }
  };
}

export const auth = createAuthStore();

// Derived stores
export const isAuthenticated = derived(auth, $auth => $auth.isAuthenticated);
export const currentUser = derived(auth, $auth => $auth.user);
export const isBusinessOwner = derived(auth, $auth => $auth.user?.user_type === 'business_owner');
export const isCustomer = derived(auth, $auth => $auth.user?.user_type === 'customer');
export const isAdmin = derived(auth, $auth => $auth.user?.is_staff || $auth.user?.is_superuser);
export const isSuperUser = derived(auth, $auth => $auth.user?.is_superuser);
export const canManageBusinesses = derived(auth, $auth => 
  $auth.user?.is_staff || 
  $auth.user?.is_superuser || 
  $auth.user?.user_type === 'business_owner'
);