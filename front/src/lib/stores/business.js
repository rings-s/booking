// src/lib/stores/business.js
import { writable, derived } from 'svelte/store';
import { businessAPI } from '$lib/api/businesses';
import toast from 'svelte-french-toast';

function createBusinessStore() {
  const { subscribe, set, update } = writable({
    businesses: [],
    currentBusiness: null,
    userBusinesses: [],
    loading: false,
    error: null,
    filters: {
      search: '',
      category: '',
      city: '',
      state: ''
    },
    pagination: {
      page: 1,
      total: 0,
      hasNext: false,
      hasPrevious: false
    }
  });

  return {
    subscribe,

    async loadBusinesses(params = {}) {
      update(state => ({ ...state, loading: true, error: null }));
      
      const { data, error } = await businessAPI.list(params);
      
      if (error) {
        update(state => ({ ...state, loading: false, error }));
        toast.error('Failed to load businesses');
      } else {
        update(state => ({
          ...state,
          businesses: data.results || [],
          pagination: {
            page: params.page || 1,
            total: data.count || 0,
            hasNext: !!data.next,
            hasPrevious: !!data.previous
          },
          loading: false
        }));
      }
    },

    async loadBusiness(slug) {
      update(state => ({ ...state, loading: true, error: null }));
      
      const { data, error } = await businessAPI.get(slug);
      
      if (error) {
        update(state => ({ ...state, loading: false, error }));
        toast.error('Failed to load business details');
        return { data: null, error };
      }
      
      update(state => ({
        ...state,
        currentBusiness: data,
        loading: false
      }));
      
      return { data, error: null };
    },

    async createBusiness(businessData) {
      update(state => ({ ...state, loading: true, error: null }));
      
      const { data, error } = await businessAPI.create(businessData);
      
      if (error) {
        update(state => ({ ...state, loading: false, error }));
        toast.error(error);
        return { data: null, error };
      }
      
      update(state => ({
        ...state,
        userBusinesses: [...state.userBusinesses, data],
        loading: false
      }));
      
      toast.success('Business created successfully');
      return { data, error: null };
    },

    async updateBusiness(slug, businessData) {
      update(state => ({ ...state, loading: true, error: null }));
      
      const { data, error } = await businessAPI.update(slug, businessData);
      
      if (error) {
        update(state => ({ ...state, loading: false, error }));
        toast.error(error);
        return { data: null, error };
      }
      
      update(state => ({
        ...state,
        currentBusiness: data,
        userBusinesses: state.userBusinesses.map(b => 
          b.slug === slug ? data : b
        ),
        loading: false
      }));
      
      toast.success('Business updated successfully');
      return { data, error: null };
    },

    async deleteBusiness(slug) {
      update(state => ({ ...state, loading: true, error: null }));
      
      const { error } = await businessAPI.delete(slug);
      
      if (error) {
        update(state => ({ ...state, loading: false, error }));
        toast.error(error);
        return { success: false, error };
      }
      
      update(state => ({
        ...state,
        userBusinesses: state.userBusinesses.filter(b => b.slug !== slug),
        loading: false
      }));
      
      toast.success('Business deleted successfully');
      return { success: true, error: null };
    },

    async loadDashboard(slug) {
      update(state => ({ ...state, loading: true, error: null }));
      
      const { data, error } = await businessAPI.getDashboard(slug);
      
      if (error) {
        update(state => ({ ...state, loading: false, error }));
        toast.error('Failed to load dashboard data');
        return { data: null, error };
      }
      
      update(state => ({ ...state, loading: false }));
      return { data, error: null };
    },

    setFilters(filters) {
      update(state => ({ ...state, filters: { ...state.filters, ...filters } }));
    },

    clearFilters() {
      update(state => ({
        ...state,
        filters: {
          search: '',
          category: '',
          city: '',
          state: ''
        }
      }));
    },

    reset() {
      set({
        businesses: [],
        currentBusiness: null,
        userBusinesses: [],
        loading: false,
        error: null,
        filters: {
          search: '',
          category: '',
          city: '',
          state: ''
        },
        pagination: {
          page: 1,
          total: 0,
          hasNext: false,
          hasPrevious: false
        }
      });
    }
  };
}

export const businessStore = createBusinessStore();

// Derived stores
export const businesses = derived(businessStore, $store => $store.businesses);
export const currentBusiness = derived(businessStore, $store => $store.currentBusiness);
export const businessLoading = derived(businessStore, $store => $store.loading);
export const businessFilters = derived(businessStore, $store => $store.filters);