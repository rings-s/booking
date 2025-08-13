// src/lib/stores/ui.js
import { writable, derived } from 'svelte/store';

function createUIStore() {
  const { subscribe, set, update } = writable({
    sidebarOpen: false,
    mobileMenuOpen: false,
    searchModalOpen: false,
    theme: 'light',
    loading: {
      global: false,
      message: ''
    },
    modals: {},
    activeTab: null,
    filters: {
      visible: false,
      applied: {}
    }
  });

  return {
    subscribe,

    toggleSidebar() {
      update(state => ({ ...state, sidebarOpen: !state.sidebarOpen }));
    },

    setSidebarOpen(open) {
      update(state => ({ ...state, sidebarOpen: open }));
    },

    toggleMobileMenu() {
      update(state => ({ ...state, mobileMenuOpen: !state.mobileMenuOpen }));
    },

    setMobileMenuOpen(open) {
      update(state => ({ ...state, mobileMenuOpen: open }));
    },

    toggleSearchModal() {
      update(state => ({ ...state, searchModalOpen: !state.searchModalOpen }));
    },

    setTheme(theme) {
      update(state => ({ ...state, theme }));
      if (typeof document !== 'undefined') {
        document.documentElement.classList.toggle('dark', theme === 'dark');
        localStorage.setItem('theme', theme);
      }
    },

    toggleTheme() {
      update(state => {
        const newTheme = state.theme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
        return { ...state, theme: newTheme };
      });
    },

    setGlobalLoading(loading, message = '') {
      update(state => ({
        ...state,
        loading: { global: loading, message }
      }));
    },

    openModal(modalId, data = {}) {
      update(state => ({
        ...state,
        modals: { ...state.modals, [modalId]: { open: true, data } }
      }));
    },

    closeModal(modalId) {
      update(state => ({
        ...state,
        modals: { ...state.modals, [modalId]: { open: false, data: {} } }
      }));
    },

    setActiveTab(tab) {
      update(state => ({ ...state, activeTab: tab }));
    },

    toggleFilters() {
      update(state => ({
        ...state,
        filters: { ...state.filters, visible: !state.filters.visible }
      }));
    },

    applyFilters(filters) {
      update(state => ({
        ...state,
        filters: { visible: state.filters.visible, applied: filters }
      }));
    },

    clearFilters() {
      update(state => ({
        ...state,
        filters: { visible: state.filters.visible, applied: {} }
      }));
    }
  };
}

export const ui = createUIStore();

// Derived stores
export const isSidebarOpen = derived(ui, $ui => $ui.sidebarOpen);
export const isMobileMenuOpen = derived(ui, $ui => $ui.mobileMenuOpen);
export const isSearchModalOpen = derived(ui, $ui => $ui.searchModalOpen);
export const theme = derived(ui, $ui => $ui.theme);
export const globalLoading = derived(ui, $ui => $ui.loading.global);
export const activeFilters = derived(ui, $ui => $ui.filters.applied);