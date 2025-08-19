import { writable, derived } from 'svelte/store';
import { locale, _, date, time, number } from 'svelte-i18n';
import { browser } from '$app/environment';
import { setLocale, getCurrentLocale, isRTL } from '../i18n/utils.js';

// Store for current locale
export const currentLocale = writable('en');

// Store for RTL direction
export const isRTLStore = derived(currentLocale, ($currentLocale) => isRTL($currentLocale));

// Store for available locales with display information
export const availableLocales = writable([
	{ code: 'en', name: 'English', flag: '🇺🇸' },
	{ code: 'ar', name: 'العربية', flag: '🇸🇦' }
]);

// Store for loading state
export const isLoadingLocale = writable(false);

// Store for locale initialization status
export const isLocaleInitialized = writable(false);

// Subscribe to svelte-i18n locale changes to update our store
if (browser) {
	locale.subscribe((value) => {
		if (value) {
			currentLocale.set(value);
			isLocaleInitialized.set(true);
		}
	});
}

/**
 * Change the current locale
 * @param {string} newLocale - The locale to switch to
 */
export async function changeLocale(newLocale) {
	if (!browser) return;
	
	isLoadingLocale.set(true);
	
	try {
		setLocale(newLocale);
		currentLocale.set(newLocale);
		
		// Update page direction and lang attributes
		document.documentElement.lang = newLocale;
		document.documentElement.dir = isRTL(newLocale) ? 'rtl' : 'ltr';
		
		// Dispatch custom event for components that need to react to locale changes
		window.dispatchEvent(new CustomEvent('localeChanged', { 
			detail: { locale: newLocale } 
		}));
		
	} catch (error) {
		console.error('Error changing locale:', error);
	} finally {
		isLoadingLocale.set(false);
	}
}

/**
 * Get translation function - re-export for convenience
 */
export { _ as t, date as tDate, time as tTime, number as tNumber };

/**
 * Translation helper with fallback
 * @param {string} key - Translation key
 * @param {Object} values - Interpolation values
 * @param {string} fallback - Fallback text if translation is missing
 * @returns {string} Translated text or fallback
 */
export function translate(key, values = {}, fallback = key) {
	let translatedText = fallback;
	
	const unsubscribe = _.subscribe((t) => {
		if (t) {
			translatedText = t(key, { values }) || fallback;
		}
	});
	
	unsubscribe();
	return translatedText;
}

/**
 * Pluralization helper
 * @param {string} key - Base translation key
 * @param {number} count - Count for pluralization
 * @param {Object} values - Additional interpolation values
 * @returns {string} Pluralized translation
 */
export function translatePlural(key, count, values = {}) {
	const pluralKey = count === 1 ? `${key}.singular` : `${key}.plural`;
	return translate(pluralKey, { count, ...values }, `${count} ${key}`);
}

/**
 * Date formatting helper
 * @param {Date|string|number} date - Date to format
 * @param {string} format - Format name (short, long, time, datetime)
 * @returns {string} Formatted date
 */
export function formatDate(date, format = 'short') {
	let formattedDate = '';
	
	const unsubscribe = tDate.subscribe((dateFormatter) => {
		if (dateFormatter) {
			formattedDate = dateFormatter(date, { format });
		}
	});
	
	unsubscribe();
	return formattedDate || new Date(date).toLocaleDateString();
}

/**
 * Number formatting helper
 * @param {number} number - Number to format
 * @param {string} format - Format name (currency, percent, decimal)
 * @returns {string} Formatted number
 */
export function formatNumber(number, format = 'decimal') {
	let formattedNumber = '';
	
	const unsubscribe = tNumber.subscribe((numberFormatter) => {
		if (numberFormatter) {
			formattedNumber = numberFormatter(number, { format });
		}
	});
	
	unsubscribe();
	return formattedNumber || number.toString();
}

/**
 * Currency formatting helper
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency code (USD, EUR, etc.)
 * @returns {string} Formatted currency
 */
export function formatCurrency(amount, currency = 'USD') {
	let formattedCurrency = '';
	
	const unsubscribe = tNumber.subscribe((numberFormatter) => {
		if (numberFormatter) {
			formattedCurrency = numberFormatter(amount, { 
				format: 'currency',
				currency 
			});
		}
	});
	
	unsubscribe();
	return formattedCurrency || `${currency} ${amount}`;
}