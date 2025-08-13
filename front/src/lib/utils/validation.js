// src/lib/utils/validation.js

/**
 * Validation utilities for forms and API inputs
 */

/**
 * Validation rule types
 */
export const ValidationRules = {
  REQUIRED: 'required',
  EMAIL: 'email',
  MIN_LENGTH: 'minLength',
  MAX_LENGTH: 'maxLength',
  PATTERN: 'pattern',
  MIN: 'min',
  MAX: 'max',
  PHONE: 'phone',
  URL: 'url',
  DATE: 'date',
  TIME: 'time',
  CUSTOM: 'custom'
};

/**
 * Common validation patterns
 */
export const ValidationPatterns = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^\+?[\d\s\-\(\)]{10,}$/,
  PASSWORD_STRONG: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/,
  URL: /^https?:\/\/[^\s$.?#].[^\s]*$/,
  SLUG: /^[a-z0-9]+(?:-[a-z0-9]+)*$/,
  TIME_24H: /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/,
  DATE_ISO: /^\d{4}-\d{2}-\d{2}$/
};

/**
 * Validation error messages
 */
export const ValidationMessages = {
  REQUIRED: 'This field is required',
  EMAIL: 'Please enter a valid email address',
  PHONE: 'Please enter a valid phone number',
  MIN_LENGTH: (min) => `Must be at least ${min} characters long`,
  MAX_LENGTH: (max) => `Must not exceed ${max} characters`,
  MIN: (min) => `Must be at least ${min}`,
  MAX: (max) => `Must not exceed ${max}`,
  PATTERN: 'Invalid format',
  URL: 'Please enter a valid URL',
  DATE: 'Please enter a valid date',
  TIME: 'Please enter a valid time',
  PASSWORD_WEAK: 'Password must contain at least 8 characters, including uppercase, lowercase, number, and special character'
};

/**
 * Validate a single field value against rules
 * @param {any} value - Value to validate
 * @param {Array|Object} rules - Validation rules
 * @returns {Object} Validation result { isValid, errors }
 */
export function validateField(value, rules) {
  const errors = [];
  
  // Normalize rules to array format
  const ruleArray = Array.isArray(rules) ? rules : [rules];
  
  for (const rule of ruleArray) {
    const error = validateSingleRule(value, rule);
    if (error) {
      errors.push(error);
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
}

/**
 * Validate a single rule against a value
 * @param {any} value - Value to validate
 * @param {Object|string} rule - Validation rule
 * @returns {string|null} Error message or null if valid
 */
function validateSingleRule(value, rule) {
  // Handle string rules (just type)
  if (typeof rule === 'string') {
    rule = { type: rule };
  }
  
  const { type, message, ...params } = rule;
  
  switch (type) {
    case ValidationRules.REQUIRED:
      if (value === null || value === undefined || value === '' || 
          (Array.isArray(value) && value.length === 0)) {
        return message || ValidationMessages.REQUIRED;
      }
      break;
      
    case ValidationRules.EMAIL:
      if (value && !ValidationPatterns.EMAIL.test(value)) {
        return message || ValidationMessages.EMAIL;
      }
      break;
      
    case ValidationRules.MIN_LENGTH:
      if (value && value.length < params.value) {
        return message || ValidationMessages.MIN_LENGTH(params.value);
      }
      break;
      
    case ValidationRules.MAX_LENGTH:
      if (value && value.length > params.value) {
        return message || ValidationMessages.MAX_LENGTH(params.value);
      }
      break;
      
    case ValidationRules.MIN:
      if (value !== null && value !== undefined && Number(value) < params.value) {
        return message || ValidationMessages.MIN(params.value);
      }
      break;
      
    case ValidationRules.MAX:
      if (value !== null && value !== undefined && Number(value) > params.value) {
        return message || ValidationMessages.MAX(params.value);
      }
      break;
      
    case ValidationRules.PATTERN:
      if (value && !params.value.test(value)) {
        return message || ValidationMessages.PATTERN;
      }
      break;
      
    case ValidationRules.PHONE:
      if (value && !ValidationPatterns.PHONE.test(value)) {
        return message || ValidationMessages.PHONE;
      }
      break;
      
    case ValidationRules.URL:
      if (value && !ValidationPatterns.URL.test(value)) {
        return message || ValidationMessages.URL;
      }
      break;
      
    case ValidationRules.DATE:
      if (value && !isValidDate(value)) {
        return message || ValidationMessages.DATE;
      }
      break;
      
    case ValidationRules.TIME:
      if (value && !ValidationPatterns.TIME_24H.test(value)) {
        return message || ValidationMessages.TIME;
      }
      break;
      
    case ValidationRules.CUSTOM:
      if (params.validator && typeof params.validator === 'function') {
        const result = params.validator(value);
        if (result !== true) {
          return message || result || 'Validation failed';
        }
      }
      break;
      
    default:
      console.warn(`Unknown validation rule type: ${type}`);
  }
  
  return null;
}

/**
 * Validate an entire form object
 * @param {Object} formData - Form data to validate
 * @param {Object} schema - Validation schema
 * @returns {Object} Validation result { isValid, errors, fieldErrors }
 */
export function validateForm(formData, schema) {
  const fieldErrors = {};
  const errors = [];
  
  for (const [fieldName, rules] of Object.entries(schema)) {
    const fieldValue = formData[fieldName];
    const validation = validateField(fieldValue, rules);
    
    if (!validation.isValid) {
      fieldErrors[fieldName] = validation.errors;
      errors.push(...validation.errors.map(error => `${fieldName}: ${error}`));
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors,
    fieldErrors
  };
}

/**
 * Create a validation schema builder
 */
export class ValidationSchemaBuilder {
  constructor() {
    this.rules = [];
  }
  
  required(message) {
    this.rules.push({ type: ValidationRules.REQUIRED, message });
    return this;
  }
  
  email(message) {
    this.rules.push({ type: ValidationRules.EMAIL, message });
    return this;
  }
  
  minLength(length, message) {
    this.rules.push({ type: ValidationRules.MIN_LENGTH, value: length, message });
    return this;
  }
  
  maxLength(length, message) {
    this.rules.push({ type: ValidationRules.MAX_LENGTH, value: length, message });
    return this;
  }
  
  min(value, message) {
    this.rules.push({ type: ValidationRules.MIN, value, message });
    return this;
  }
  
  max(value, message) {
    this.rules.push({ type: ValidationRules.MAX, value, message });
    return this;
  }
  
  pattern(regex, message) {
    this.rules.push({ type: ValidationRules.PATTERN, value: regex, message });
    return this;
  }
  
  phone(message) {
    this.rules.push({ type: ValidationRules.PHONE, message });
    return this;
  }
  
  url(message) {
    this.rules.push({ type: ValidationRules.URL, message });
    return this;
  }
  
  custom(validator, message) {
    this.rules.push({ type: ValidationRules.CUSTOM, validator, message });
    return this;
  }
  
  build() {
    return this.rules;
  }
}

/**
 * Helper function to create validation rules
 */
export const v = new ValidationSchemaBuilder();

/**
 * Common validation schemas
 */
export const CommonSchemas = {
  email: () => new ValidationSchemaBuilder().required().email().build(),
  password: () => new ValidationSchemaBuilder()
    .required()
    .minLength(8)
    .pattern(ValidationPatterns.PASSWORD_STRONG, ValidationMessages.PASSWORD_WEAK)
    .build(),
  phone: () => new ValidationSchemaBuilder().phone().build(),
  url: () => new ValidationSchemaBuilder().url().build(),
  name: () => new ValidationSchemaBuilder()
    .required()
    .minLength(2)
    .maxLength(50)
    .build()
};

/**
 * Utility functions
 */

/**
 * Check if a date string is valid
 */
function isValidDate(dateString) {
  if (!dateString) return false;
  
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date);
}

/**
 * Sanitize form data by trimming strings and removing empty values
 * @param {Object} formData - Form data to sanitize
 * @param {Object} options - Sanitization options
 * @returns {Object} Sanitized form data
 */
export function sanitizeFormData(formData, options = {}) {
  const { 
    trimStrings = true,
    removeEmpty = false,
    removeNull = false,
    removeUndefined = true 
  } = options;
  
  const sanitized = {};
  
  for (const [key, value] of Object.entries(formData)) {
    let sanitizedValue = value;
    
    // Trim strings
    if (trimStrings && typeof value === 'string') {
      sanitizedValue = value.trim();
    }
    
    // Skip empty values if requested
    if (removeEmpty && sanitizedValue === '') {
      continue;
    }
    
    // Skip null values if requested
    if (removeNull && sanitizedValue === null) {
      continue;
    }
    
    // Skip undefined values if requested
    if (removeUndefined && sanitizedValue === undefined) {
      continue;
    }
    
    sanitized[key] = sanitizedValue;
  }
  
  return sanitized;
}

/**
 * Validate API response data
 * @param {any} data - Response data to validate
 * @param {Object} expectedStructure - Expected data structure
 * @returns {boolean} True if data matches expected structure
 */
export function validateApiResponse(data, expectedStructure) {
  if (!data || typeof data !== 'object') {
    return false;
  }
  
  for (const [key, type] of Object.entries(expectedStructure)) {
    if (!(key in data)) {
      console.warn(`Missing required field: ${key}`);
      return false;
    }
    
    const actualType = typeof data[key];
    if (actualType !== type) {
      console.warn(`Type mismatch for field ${key}: expected ${type}, got ${actualType}`);
      return false;
    }
  }
  
  return true;
}

/**
 * Create a debounced validation function
 * @param {Function} validator - Validation function
 * @param {number} delay - Debounce delay in milliseconds
 * @returns {Function} Debounced validation function
 */
export function createDebouncedValidator(validator, delay = 300) {
  let timeoutId;
  
  return function debouncedValidator(...args) {
    return new Promise((resolve) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        resolve(validator(...args));
      }, delay);
    });
  };
}

/**
 * Real-time form validation hook
 * @param {Object} formData - Form data object
 * @param {Object} schema - Validation schema
 * @returns {Object} Validation state and methods
 */
export function useFormValidation(formData, schema) {
  const validation = validateForm(formData, schema);
  
  return {
    ...validation,
    
    // Validate single field
    validateField: (fieldName) => {
      const rules = schema[fieldName];
      if (!rules) return { isValid: true, errors: [] };
      
      const fieldValue = formData[fieldName];
      return validateField(fieldValue, rules);
    },
    
    // Check if form is ready to submit
    canSubmit: () => validation.isValid && Object.keys(formData).length > 0,
    
    // Get first error for a field
    getFieldError: (fieldName) => {
      const fieldErrors = validation.fieldErrors[fieldName];
      return fieldErrors && fieldErrors.length > 0 ? fieldErrors[0] : null;
    }
  };
}