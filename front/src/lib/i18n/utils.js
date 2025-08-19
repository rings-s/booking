import { browser } from '$app/environment';
import { locale, waitLocale } from 'svelte-i18n';
import { supportedLocales, defaultLocale } from './index.js';

/**
 * Set the current locale and persist it to localStorage
 * @param {string} newLocale - The locale to set
 */
export function setLocale(newLocale) {
	if (!supportedLocales.includes(newLocale)) {
		console.warn(`Locale "${newLocale}" is not supported. Using default locale "${defaultLocale}".`);
		newLocale = defaultLocale;
	}

	locale.set(newLocale);
	
	if (browser) {
		localStorage.setItem('locale', newLocale);
		// Update document lang attribute for accessibility
		document.documentElement.lang = newLocale;
		// Update document dir attribute for RTL languages
		document.documentElement.dir = newLocale === 'ar' ? 'rtl' : 'ltr';
	}
}

/**
 * Get the current locale
 * @returns {string} Current locale
 */
export function getCurrentLocale() {
	let currentLocale;
	locale.subscribe((value) => {
		currentLocale = value;
	})();
	return currentLocale || defaultLocale;
}

/**
 * Check if a locale is RTL (Right-to-Left)
 * @param {string} localeCode - The locale to check
 * @returns {boolean} Whether the locale is RTL
 */
export function isRTL(localeCode = null) {
	const checkLocale = localeCode || getCurrentLocale();
	const rtlLocales = ['ar', 'he', 'fa', 'ur'];
	return rtlLocales.includes(checkLocale);
}

/**
 * Get the display name of a locale in its own language
 * @param {string} localeCode - The locale code
 * @returns {string} Display name
 */
export function getLocaleDisplayName(localeCode) {
	const displayNames = {
		en: 'English',
		es: 'Español',
		fr: 'Français',
		de: 'Deutsch',
		ar: 'العربية'
	};
	return displayNames[localeCode] || localeCode;
}

/**
 * Get flag emoji for a locale
 * @param {string} localeCode - The locale code
 * @returns {string} Flag emoji
 */
export function getLocaleFlag(localeCode) {
	const flags = {
		en: '🇺🇸',
		es: '🇪🇸',
		fr: '🇫🇷',
		de: '🇩🇪',
		ar: '🇸🇦'
	};
	return flags[localeCode] || '🌐';
}

/**
 * Wait for locale to be loaded and return a promise
 * Useful for SSR and ensuring translations are loaded before rendering
 * @returns {Promise} Promise that resolves when locale is loaded
 */
export function ensureLocaleLoaded() {
	return waitLocale();
}