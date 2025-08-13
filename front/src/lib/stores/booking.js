// src/lib/stores/booking.js
import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';
import { bookingAPI } from '$lib/api/bookings';
import { businessAPI } from '$lib/api/businesses';

function createBookingStore() {
  const { subscribe, set, update } = writable({
    bookings: [],
    currentBooking: null,
    isLoading: false,
    error: null
  });

  return {
    subscribe,
    
    async createBooking(bookingData) {
      update(state => ({ ...state, isLoading: true, error: null }));
      
      try {
        const { data, error } = await bookingAPI.create(bookingData);
        
        if (error) {
          update(state => ({ ...state, isLoading: false, error }));
          return { data: null, error };
        }
        
        update(state => ({
          ...state,
          isLoading: false,
          bookings: [...state.bookings, data],
          currentBooking: data
        }));
        
        return { data, error: null };
      } catch (err) {
        const error = err.message || 'Failed to create booking';
        update(state => ({ ...state, isLoading: false, error }));
        return { data: null, error };
      }
    },
    
    async updateBooking(id, bookingData) {
      update(state => ({ ...state, isLoading: true, error: null }));
      
      try {
        const { data, error } = await bookingAPI.update(id, bookingData);
        
        if (error) {
          update(state => ({ ...state, isLoading: false, error }));
          return { data: null, error };
        }
        
        update(state => ({
          ...state,
          isLoading: false,
          bookings: state.bookings.map(b => b.id === id ? data : b),
          currentBooking: data
        }));
        
        return { data, error: null };
      } catch (err) {
        const error = err.message || 'Failed to update booking';
        update(state => ({ ...state, isLoading: false, error }));
        return { data: null, error };
      }
    },
    
    async loadAvailableSlots(businessSlug, serviceId, date) {
      try {
        const { data, error } = await businessAPI.getAvailableSlots(businessSlug, serviceId, date);
        return { data, error };
      } catch (err) {
        return { data: null, error: err.message || 'Failed to load available slots' };
      }
    },

    async loadAvailableDates(businessSlug, serviceId, daysAhead = 90) {
      try {
        const { data, error } = await businessAPI.getAvailableDates(businessSlug, serviceId, daysAhead);
        return { data, error };
      } catch (err) {
        return { data: null, error: err.message || 'Failed to load available dates' };
      }
    },
    
    async loadBookings(filters = {}) {
      update(state => ({ ...state, isLoading: true, error: null }));
      
      try {
        const { data, error } = await bookingAPI.list(filters);
        
        if (error) {
          update(state => ({ ...state, isLoading: false, error }));
          return { data: null, error };
        }
        
        update(state => ({
          ...state,
          isLoading: false,
          bookings: data.results || data
        }));
        
        return { data, error: null };
      } catch (err) {
        const error = err.message || 'Failed to load bookings';
        update(state => ({ ...state, isLoading: false, error }));
        return { data: null, error };
      }
    },
    
    async cancelBooking(id) {
      try {
        const { data, error } = await bookingAPI.cancel(id);
        
        if (!error && data) {
          update(state => ({
            ...state,
            bookings: state.bookings.map(b => b.id === id ? data : b)
          }));
        }
        
        return { data, error };
      } catch (err) {
        return { data: null, error: err.message || 'Failed to cancel booking' };
      }
    },
    
    clearError() {
      update(state => ({ ...state, error: null }));
    },
    
    reset() {
      set({
        bookings: [],
        currentBooking: null,
        isLoading: false,
        error: null
      });
    }
  };
}

export const bookingStore = createBookingStore();

// Derived stores
export const currentBooking = derived(bookingStore, $store => $store.currentBooking);
export const isBookingLoading = derived(bookingStore, $store => $store.isLoading);
export const bookingError = derived(bookingStore, $store => $store.error);