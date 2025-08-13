// src/lib/utils/validators.js
import * as yup from 'yup';

// Email validation
export const emailSchema = yup.string()
  .email('Invalid email address')
  .required('Email is required');

// Password validation
export const passwordSchema = yup.string()
  .min(8, 'Password must be at least 8 characters')
  .matches(/[a-z]/, 'Password must contain at least one lowercase letter')
  .matches(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .matches(/[0-9]/, 'Password must contain at least one number')
  .required('Password is required');

// Phone validation
export const phoneSchema = yup.string()
  .matches(/^[\d\s\-\+\(\)]+$/, 'Invalid phone number')
  .min(10, 'Phone number must be at least 10 digits')
  .required('Phone number is required');

// Business validation schema
export const businessSchema = yup.object({
  name: yup.string().required('Business name is required'),
  email: emailSchema,
  phone: phoneSchema,
  description: yup.string().min(50, 'Description must be at least 50 characters'),
  address: yup.string().required('Address is required'),
  city: yup.string().required('City is required'),
  state: yup.string().required('State is required'),
  country: yup.string().required('Country is required'),
  postal_code: yup.string().required('Postal code is required'),
  category: yup.string().required('Category is required')
});

// Service validation schema
export const serviceSchema = yup.object({
  name: yup.string().required('Service name is required'),
  description: yup.string().required('Description is required'),
  duration_minutes: yup.number()
    .min(15, 'Duration must be at least 15 minutes')
    .required('Duration is required'),
  price: yup.number()
    .min(0, 'Price must be positive')
    .required('Price is required')
});

// Booking validation schema
export const bookingSchema = yup.object({
  service_id: yup.string().required('Service is required'),
  booking_date: yup.date()
    .min(new Date(), 'Booking date must be in the future')
    .required('Date is required'),
  start_time: yup.string().required('Time is required'),
  notes: yup.string().max(500, 'Notes must be less than 500 characters')
});

// Registration validation schema
export const registrationSchema = yup.object({
  first_name: yup.string()
    .min(2, 'First name must be at least 2 characters')
    .max(50, 'First name must be less than 50 characters')
    .matches(/^[a-zA-Z\s'-]+$/, 'First name can only contain letters, spaces, apostrophes, and hyphens')
    .required('First name is required'),
  last_name: yup.string()
    .min(2, 'Last name must be at least 2 characters')
    .max(50, 'Last name must be less than 50 characters')
    .matches(/^[a-zA-Z\s'-]+$/, 'Last name can only contain letters, spaces, apostrophes, and hyphens')
    .required('Last name is required'),
  email: emailSchema,
  password: passwordSchema,
  password_confirm: yup.string()
    .oneOf([yup.ref('password'), null], 'Passwords must match')
    .required('Password confirmation is required'),
  phone: yup.string()
    .matches(/^[\d\s\-\+\(\)]+$/, 'Invalid phone number format')
    .min(10, 'Phone number must be at least 10 digits'),
  terms_accepted: yup.boolean()
    .oneOf([true], 'You must accept the terms and conditions')
});

// Review validation schema
export const reviewSchema = yup.object({
  rating: yup.number()
    .min(1, 'Rating must be at least 1')
    .max(5, 'Rating must be at most 5')
    .required('Rating is required'),
  title: yup.string()
    .max(200, 'Title must be less than 200 characters')
    .required('Title is required'),
  comment: yup.string()
    .min(10, 'Comment must be at least 10 characters')
    .max(1000, 'Comment must be less than 1000 characters')
    .required('Comment is required')
});

// Generic validation function
export async function validateForm(schema, data) {
  try {
    await schema.validate(data, { abortEarly: false });
    return { isValid: true, errors: {} };
  } catch (error) {
    const errors = {};
    error.inner.forEach(err => {
      errors[err.path] = err.message;
    });
    return { isValid: false, errors };
  }
}