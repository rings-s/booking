// src/lib/utils/formatters.js
import { format, parseISO, formatDistanceToNow } from 'date-fns';

// Format currency
export function formatCurrency(amount, currency = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency
  }).format(amount);
}

// Format date
export function formatDate(date, formatString = 'MMM dd, yyyy') {
  if (!date) return '';
  const dateObj = typeof date === 'string' ? parseISO(date) : date;
  return format(dateObj, formatString);
}

// Format time
export function formatTime(time, format24h = false) {
  if (!time) return '';
  const formatString = format24h ? 'HH:mm' : 'h:mm a';
  
  if (typeof time === 'string' && time.includes(':')) {
    const [hours, minutes] = time.split(':');
    const date = new Date();
    date.setHours(parseInt(hours), parseInt(minutes));
    return format(date, formatString);
  }
  
  return format(time, formatString);
}

// Format relative time
export function formatRelativeTime(date) {
  if (!date) return '';
  const dateObj = typeof date === 'string' ? parseISO(date) : date;
  return formatDistanceToNow(dateObj, { addSuffix: true });
}

// Format phone number
export function formatPhone(phone) {
  if (!phone) return '';
  const cleaned = phone.replace(/\D/g, '');
  const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
  if (match) {
    return '(' + match[1] + ') ' + match[2] + '-' + match[3];
  }
  return phone;
}

// Format file size
export function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Format percentage
export function formatPercentage(value, decimals = 0) {
  return `${(value * 100).toFixed(decimals)}%`;
}

// Format duration
export function formatDuration(minutes) {
  if (!minutes) return '';
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  
  if (hours === 0) return `${mins} min`;
  if (mins === 0) return `${hours} hr`;
  return `${hours} hr ${mins} min`;
}

// Format address
export function formatAddress(address) {
  const { street, city, state, postal_code, country } = address;
  const parts = [street, city, state, postal_code, country].filter(Boolean);
  return parts.join(', ');
}

// Format booking status
export function formatBookingStatus(status) {
  const statusMap = {
    pending: 'Pending',
    confirmed: 'Confirmed',
    cancelled: 'Cancelled',
    completed: 'Completed',
    no_show: 'No Show'
  };
  return statusMap[status] || status;
}

// Truncate text
export function truncateText(text, maxLength = 100) {
  if (!text || text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

// Slugify text
export function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim();
}

// Format number with thousands separator
export function formatNumber(value) {
  if (value === null || value === undefined || isNaN(value)) {
    return '0';
  }
  return new Intl.NumberFormat('en-US').format(Number(value));
}

// Format decimal values
export function formatDecimal(value, decimals = 1) {
  if (value === null || value === undefined || isNaN(value)) {
    return '0.0';
  }
  return Number(value).toFixed(decimals);
}

// Format chart data for Chart.js
export function formatChartData(data, labelKey = 'label', valueKey = 'value') {
  if (!Array.isArray(data)) return { labels: [], data: [] };
  
  return {
    labels: data.map(item => item[labelKey] || ''),
    data: data.map(item => item[valueKey] || 0)
  };
}

// Format data for charts with multiple datasets
export function formatMultiDatasetChart(data, labelKey = 'label', datasets = []) {
  if (!Array.isArray(data)) return { labels: [], datasets: [] };
  
  const labels = data.map(item => item[labelKey] || '');
  const formattedDatasets = datasets.map(dataset => ({
    ...dataset,
    data: data.map(item => item[dataset.key] || 0)
  }));
  
  return {
    labels,
    datasets: formattedDatasets
  };
}

// Format rating display
export function formatRating(rating, maxRating = 5) {
  if (!rating && rating !== 0) return 'No rating';
  
  const stars = '★'.repeat(Math.floor(rating)) + '☆'.repeat(maxRating - Math.floor(rating));
  return `${stars} (${formatDecimal(rating, 1)})`;
}

// Format change indicators (for stats cards)
export function formatChange(value, format = 'percentage') {
  if (value === null || value === undefined || isNaN(value)) {
    return { text: '0%', positive: true };
  }
  
  const numValue = Number(value);
  const isPositive = numValue >= 0;
  const prefix = isPositive ? '+' : '';
  
  let text = '';
  switch (format) {
    case 'percentage':
      text = `${prefix}${formatPercentage(Math.abs(numValue))}`;
      break;
    case 'currency':
      text = `${prefix}${formatCurrency(Math.abs(numValue))}`;
      break;
    case 'number':
      text = `${prefix}${formatNumber(Math.abs(numValue))}`;
      break;
    default:
      text = `${prefix}${numValue}`;
  }
  
  return {
    text,
    positive: isPositive
  };
}

// Format business hours
export function formatBusinessHours(hours) {
  if (!hours || hours.is_closed) {
    return 'Closed';
  }
  
  const openTime = formatTime(hours.opening_time);
  const closeTime = formatTime(hours.closing_time);
  
  return `${openTime} - ${closeTime}`;
}

// Format table values with type detection
export function formatTableValue(value, type = 'text') {
  switch (type) {
    case 'currency':
      return formatCurrency(value);
    case 'number':
      return formatNumber(value);
    case 'percentage':
      return formatPercentage(value);
    case 'decimal':
      return formatDecimal(value);
    case 'date':
      return formatDate(value);
    case 'time':
      return formatTime(value);
    case 'relative':
      return formatRelativeTime(value);
    case 'phone':
      return formatPhone(value);
    case 'rating':
      return formatRating(value);
    default:
      return value || '';
  }
}