// src/lib/utils/constants.js

export const BOOKING_STATUS = {
    PENDING: 'pending',
    CONFIRMED: 'confirmed',
    CANCELLED: 'cancelled',
    COMPLETED: 'completed',
    NO_SHOW: 'no_show'
  };
  
  export const USER_TYPES = {
    CUSTOMER: 'customer',
    BUSINESS_OWNER: 'business_owner',
    ADMIN: 'admin'
  };
  
  export const SUBSCRIPTION_PLANS = {
    FREE: 'free',
    BASIC: 'basic',
    PREMIUM: 'premium',
    ENTERPRISE: 'enterprise'
  };
  
  export const NOTIFICATION_TYPES = {
    BOOKING_CONFIRMED: 'booking_confirmed',
    BOOKING_CANCELLED: 'booking_cancelled',
    BOOKING_REMINDER: 'booking_reminder',
    REVIEW_REQUEST: 'review_request',
    PAYMENT_RECEIVED: 'payment_received',
    SUBSCRIPTION_EXPIRING: 'subscription_expiring',
    NEW_CUSTOMER: 'new_customer',
    GENERAL: 'general'
  };
  
  export const WEEKDAYS = [
    { value: 0, label: 'Monday', short: 'Mon' },
    { value: 1, label: 'Tuesday', short: 'Tue' },
    { value: 2, label: 'Wednesday', short: 'Wed' },
    { value: 3, label: 'Thursday', short: 'Thu' },
    { value: 4, label: 'Friday', short: 'Fri' },
    { value: 5, label: 'Saturday', short: 'Sat' },
    { value: 6, label: 'Sunday', short: 'Sun' }
  ];
  
  export const BUSINESS_CATEGORIES = [
    'Salon & Spa',
    'Health & Wellness',
    'Fitness',
    'Medical',
    'Dental',
    'Automotive',
    'Home Services',
    'Professional Services',
    'Education',
    'Restaurant',
    'Entertainment',
    'Other'
  ];
  
  export const TIME_SLOTS = [
    '08:00', '08:30', '09:00', '09:30', '10:00', '10:30',
    '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
    '14:00', '14:30', '15:00', '15:30', '16:00', '16:30',
    '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
    '20:00', '20:30', '21:00'
  ];
  
  export const DURATIONS = [
    { value: 15, label: '15 minutes' },
    { value: 30, label: '30 minutes' },
    { value: 45, label: '45 minutes' },
    { value: 60, label: '1 hour' },
    { value: 90, label: '1.5 hours' },
    { value: 120, label: '2 hours' },
    { value: 180, label: '3 hours' },
    { value: 240, label: '4 hours' }
  ];
  
  export const CHART_COLORS = {
    primary: '#4f46e5',
    secondary: '#06b6d4',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#3b82f6'
  };
  
  export const API_ENDPOINTS = {
    AUTH: '/accounts',
    BUSINESSES: '/businesses',
    SERVICES: '/services',
    BOOKINGS: '/bookings',
    CUSTOMERS: '/customers',
    REVIEWS: '/reviews',
    NOTIFICATIONS: '/notifications'
  };
  
  export const ERROR_MESSAGES = {
    NETWORK_ERROR: 'Network error. Please check your connection.',
    UNAUTHORIZED: 'You need to be logged in to perform this action.',
    FORBIDDEN: 'You do not have permission to perform this action.',
    NOT_FOUND: 'The requested resource was not found.',
    SERVER_ERROR: 'Server error. Please try again later.',
    VALIDATION_ERROR: 'Please check your input and try again.'
  };
  
  export const SUCCESS_MESSAGES = {
    BOOKING_CREATED: 'Your booking has been created successfully!',
    BOOKING_CANCELLED: 'Your booking has been cancelled.',
    REVIEW_SUBMITTED: 'Thank you for your review!',
    PROFILE_UPDATED: 'Your profile has been updated.',
    BUSINESS_CREATED: 'Your business has been created successfully!',
    SERVICE_ADDED: 'Service has been added successfully!'
  };
  
  export const REGEX_PATTERNS = {
    EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    PHONE: /^[\d\s\-\+\(\)]+$/,
    POSTAL_CODE: /^[A-Z0-9\s\-]+$/i,
    SLUG: /^[a-z0-9\-]+$/
  };