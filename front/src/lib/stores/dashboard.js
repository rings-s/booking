// src/lib/stores/dashboard.js
import { writable, derived, readable } from 'svelte/store';
import { businessAPI } from '$lib/api/businesses';
import { bookingAPI } from '$lib/api/bookings';
import { get } from 'svelte/store';
import toast from 'svelte-french-toast';

/**
 * Dashboard Store - Comprehensive state management for business dashboard
 * Features:
 * - Real-time data fetching from backend APIs
 * - Caching with automatic refresh
 * - Error handling and loading states
 * - Multiple data sources and chart data
 * - Period-based filtering (week, month, quarter, year)
 */

// Core loading and error states
export const loading = writable(false);
export const error = writable(null);
export const lastUpdated = writable(null);

// Dashboard configuration
export const activePeriod = writable('month');
export const autoRefresh = writable(true);
export const refreshInterval = writable(5 * 60 * 1000); // 5 minutes

// Main dashboard data store
export const dashboardData = writable({
  total_bookings: 0,
  total_revenue: 0,
  total_customers: 0,
  average_rating: 0,
  bookings_growth: 0,
  revenue_growth: 0,
  bookings_by_date: [],
  revenue_by_month: [],
  bookings_by_hour: [],
  bookings_by_weekday: [],
  popular_services: [],
  service_revenue: [],
  customer_demographics: {},
  top_customers: [],
  customer_retention: {},
  recent_bookings: [],
  recent_reviews: [],
  booking_status_breakdown: [],
  next_week_bookings: 0
});

// Individual data stores for charts
export const statsData = writable({
  revenue: 0,
  bookings: 0,
  confirmed_bookings: 0,
  customers: 0,
  rating: 0,
  revenueChange: 0,
  bookingsChange: 0,
  customersChange: 0,
  ratingChange: 0
});

export const revenueData = writable([]);
export const bookingChartData = writable([]);
export const serviceStats = writable([]);
export const recentActivity = writable([]);

// Derived stores for computed values
export const totalRevenue = derived(dashboardData, $data => $data.total_revenue || 0);
export const totalBookings = derived(dashboardData, $data => $data.total_bookings || 0);
export const averageRating = derived(dashboardData, $data => $data.average_rating || 0);
export const revenueGrowth = derived(dashboardData, $data => $data.revenue_growth || 0);
export const bookingsGrowth = derived(dashboardData, $data => $data.bookings_growth || 0);

// Popular services with calculations
export const popularServices = derived(dashboardData, $data => {
  const services = $data.popular_services || [];
  return services.map(service => ({
    ...service,
    revenue_percentage: $data.total_revenue > 0 ? 
      ((service.revenue || 0) / $data.total_revenue * 100).toFixed(1) : 0,
    bookings_percentage: $data.total_bookings > 0 ? 
      ((service.bookings || 0) / $data.total_bookings * 100).toFixed(1) : 0
  }));
});

// Customer metrics
export const customerMetrics = derived(dashboardData, $data => {
  const demographics = $data.customer_demographics || {};
  const retention = $data.customer_retention || {};
  
  return {
    total: demographics.total || 0,
    new_this_month: demographics.new_this_month || 0,
    returning: demographics.returning || 0,
    retention_rate: retention.rate || 0,
    retained_customers: retention.retained || 0
  };
});

// Booking trends for charts
export const bookingTrends = derived(dashboardData, $data => {
  const byDate = $data.bookings_by_date || [];
  const byHour = $data.bookings_by_hour || [];
  const byWeekday = $data.bookings_by_weekday || [];
  
  return {
    daily: byDate.map(item => ({
      date: item.date,
      bookings: item.bookings || 0,
      revenue: item.revenue || 0
    })),
    hourly: byHour.map(item => ({
      hour: item.hour,
      count: item.count || 0
    })),
    weekly: byWeekday.map(item => ({
      weekday: item.weekday,
      count: item.count || 0
    }))
  };
});

// Revenue trends for charts
export const revenueTrends = derived([dashboardData, revenueData], ([$dashboard, $revenue]) => {
  // Combine dashboard revenue data with detailed revenue data
  const monthlyRevenue = $dashboard.revenue_by_month || [];
  const dailyRevenue = $revenue || [];
  
  return {
    monthly: monthlyRevenue.map(item => ({
      month: item.month,
      revenue: item.revenue || 0
    })),
    daily: dailyRevenue.map(item => ({
      date: item.date,
      revenue: item.revenue || 0
    }))
  };
});

// Is data stale checker
export const isDataStale = derived([lastUpdated, refreshInterval], ([$lastUpdated, $interval]) => {
  if (!$lastUpdated) return true;
  return Date.now() - $lastUpdated > $interval;
});

// Dashboard store with methods
function createDashboardStore() {
  let refreshTimer;
  let businessSlug = null;
  
  return {
    subscribe: dashboardData.subscribe,
    
    // Initialize dashboard for a specific business
    async init(slug) {
      businessSlug = slug;
      await this.loadDashboard();
      this.startAutoRefresh();
    },
    
    // Load main dashboard data
    async loadDashboard() {
      if (!businessSlug) {
        console.warn('Dashboard: No business slug provided');
        return;
      }
      
      loading.set(true);
      error.set(null);
      
      try {
        const { data, error: apiError } = await businessAPI.dashboard(businessSlug);
        
        if (apiError) {
          throw new Error(apiError);
        }
        
        if (!data) {
          throw new Error('No dashboard data received');
        }
        dashboardData.set(data);
        lastUpdated.set(Date.now());
        
        // Load additional data in parallel
        await Promise.allSettled([
          this.loadStats(),
          this.loadRevenueData(),
          this.loadServiceStats(),
          this.loadRecentActivity()
        ]);
        
      } catch (err) {
        console.error('Dashboard load error:', err);
        error.set(err.message || 'Failed to load dashboard data');
        toast.error('Failed to load dashboard data');
      } finally {
        loading.set(false);
      }
    },
    
    // Load statistics data
    async loadStats(period = null) {
      if (!businessSlug) return;
      
      try {
        const params = period ? { period } : { period: get(activePeriod) };
        const { data, error: apiError } = await businessAPI.stats(businessSlug, params);
        
        if (apiError) {
          console.warn('Stats load error:', apiError);
          return;
        }
        
        statsData.set(data);
      } catch (err) {
        console.error('Stats load error:', err);
      }
    },
    
    // Load revenue data for charts
    async loadRevenueData(period = null) {
      if (!businessSlug) return;
      
      try {
        const params = period ? { period } : { period: get(activePeriod) };
        const { data, error: apiError } = await businessAPI.revenueData(businessSlug, params);
        
        if (apiError) {
          console.warn('Revenue data load error:', apiError);
          return;
        }
        
        revenueData.set(data || []);
      } catch (err) {
        console.error('Revenue data load error:', err);
      }
    },
    
    // Load service statistics
    async loadServiceStats() {
      if (!businessSlug) return;
      
      try {
        const { data, error: apiError } = await businessAPI.serviceStats(businessSlug);
        
        if (apiError) {
          console.warn('Service stats load error:', apiError);
          return;
        }
        
        serviceStats.set(data || []);
      } catch (err) {
        console.error('Service stats load error:', err);
      }
    },
    
    // Load recent activity
    async loadRecentActivity() {
      if (!businessSlug) return;
      
      try {
        const { data, error: apiError } = await businessAPI.recentActivity(businessSlug);
        
        if (apiError) {
          console.warn('Recent activity load error:', apiError);
          return;
        }
        
        recentActivity.set(data || []);
      } catch (err) {
        console.error('Recent activity load error:', err);
      }
    },
    
    // Load booking chart data
    async loadBookingChartData(period = null) {
      try {
        const params = period ? { period } : { period: get(activePeriod) };
        const { data, error: apiError } = await bookingAPI.chartData(params);
        
        if (apiError) {
          console.warn('Booking chart data load error:', apiError);
          return;
        }
        
        bookingChartData.set(data || []);
      } catch (err) {
        console.error('Booking chart data load error:', err);
      }
    },
    
    // Refresh all data
    async refresh() {
      if (get(loading)) return; // Prevent concurrent refreshes
      
      await this.loadDashboard();
    },
    
    // Change active period and reload data
    async changePeriod(newPeriod) {
      activePeriod.set(newPeriod);
      
      // Reload period-dependent data
      await Promise.allSettled([
        this.loadStats(newPeriod),
        this.loadRevenueData(newPeriod),
        this.loadBookingChartData(newPeriod)
      ]);
    },
    
    // Start auto-refresh timer
    startAutoRefresh() {
      this.stopAutoRefresh();
      
      if (get(autoRefresh)) {
        refreshTimer = setInterval(() => {
          if (get(isDataStale)) {
            this.refresh();
          }
        }, get(refreshInterval));
      }
    },
    
    // Stop auto-refresh timer
    stopAutoRefresh() {
      if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
      }
    },
    
    // Force refresh specific data type
    async refreshData(dataType, options = {}) {
      switch (dataType) {
        case 'stats':
          await this.loadStats(options.period);
          break;
        case 'revenue':
          await this.loadRevenueData(options.period);
          break;
        case 'services':
          await this.loadServiceStats();
          break;
        case 'activity':
          await this.loadRecentActivity();
          break;
        case 'bookings':
          await this.loadBookingChartData(options.period);
          break;
        default:
          await this.refresh();
      }
    },
    
    // Clear all data (for logout or business change)
    clear() {
      this.stopAutoRefresh();
      businessSlug = null;
      
      dashboardData.set({
        total_bookings: 0,
        total_revenue: 0,
        total_customers: 0,
        average_rating: 0,
        bookings_growth: 0,
        revenue_growth: 0,
        bookings_by_date: [],
        revenue_by_month: [],
        bookings_by_hour: [],
        bookings_by_weekday: [],
        popular_services: [],
        service_revenue: [],
        customer_demographics: {},
        top_customers: [],
        customer_retention: {},
        recent_bookings: [],
        recent_reviews: [],
        booking_status_breakdown: [],
        next_week_bookings: 0
      });
      
      statsData.set({
        revenue: 0,
        bookings: 0,
        confirmed_bookings: 0,
        customers: 0,
        rating: 0,
        revenueChange: 0,
        bookingsChange: 0,
        customersChange: 0,
        ratingChange: 0
      });
      
      revenueData.set([]);
      bookingChartData.set([]);
      serviceStats.set([]);
      recentActivity.set([]);
      
      loading.set(false);
      error.set(null);
      lastUpdated.set(null);
    },
    
    // Get current business slug
    getBusinessSlug() {
      return businessSlug;
    }
  };
}

// Export the dashboard store instance
export const dashboard = createDashboardStore();

// Cleanup on page unload
if (typeof window !== 'undefined') {
  window.addEventListener('beforeunload', () => {
    dashboard.stopAutoRefresh();
  });
}

// Export convenience functions
export const refreshDashboard = () => dashboard.refresh();
export const changeDashboardPeriod = (period) => dashboard.changePeriod(period);
export const initDashboard = (slug) => dashboard.init(slug);
export const clearDashboard = () => dashboard.clear();