// src/lib/stores/cart.js
import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

function createCartStore() {
  // Load initial cart from localStorage
  const initialCart = browser ? JSON.parse(localStorage.getItem('booking_cart') || '[]') : [];
  
  const { subscribe, set, update } = writable({
    items: initialCart,
    business: null,
    total: 0
  });

  // Save to localStorage whenever cart changes
  subscribe(value => {
    if (browser) {
      localStorage.setItem('booking_cart', JSON.stringify(value.items));
    }
  });

  return {
    subscribe,

    addItem(service, business, date, time) {
      update(state => {
        // Check if adding service from different business
        if (state.business && state.business.id !== business.id) {
          if (!confirm('Adding services from a different business will clear your current cart. Continue?')) {
            return state;
          }
          // Clear cart if different business
          return {
            items: [{
              id: `${service.id}-${date}-${time}`,
              service,
              business,
              date,
              time,
              price: service.price
            }],
            business,
            total: service.price
          };
        }

        // Check if item already exists
        const existingItem = state.items.find(
          item => item.service.id === service.id && item.date === date && item.time === time
        );

        if (existingItem) {
          return state; // Item already in cart
        }

        const newItem = {
          id: `${service.id}-${date}-${time}`,
          service,
          business,
          date,
          time,
          price: service.price
        };

        const items = [...state.items, newItem];
        const total = items.reduce((sum, item) => sum + parseFloat(item.price), 0);

        return {
          items,
          business: business,
          total
        };
      });
    },

    removeItem(itemId) {
      update(state => {
        const items = state.items.filter(item => item.id !== itemId);
        const total = items.reduce((sum, item) => sum + parseFloat(item.price), 0);
        
        return {
          items,
          business: items.length > 0 ? state.business : null,
          total
        };
      });
    },

    clearCart() {
      set({
        items: [],
        business: null,
        total: 0
      });
    },

    updateItemTime(itemId, newTime) {
      update(state => {
        const items = state.items.map(item => 
          item.id === itemId 
            ? { ...item, time: newTime, id: `${item.service.id}-${item.date}-${newTime}` }
            : item
        );
        
        return { ...state, items };
      });
    }
  };
}

export const cart = createCartStore();

// Derived stores
export const cartItems = derived(cart, $cart => $cart.items);
export const cartTotal = derived(cart, $cart => $cart.total);
export const cartCount = derived(cart, $cart => $cart.items.length);
export const cartBusiness = derived(cart, $cart => $cart.business);