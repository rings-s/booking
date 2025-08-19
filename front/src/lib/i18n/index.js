import { browser } from '$app/environment';
import { init, register } from 'svelte-i18n';

const defaultLocale = 'en';

const supportedLocales = ['en', 'ar'];

// Register supported locales
register('en', () => import('./locales/en.json'));
register('ar', () => import('./locales/ar.json'));

// Utility function to detect user's preferred language
function detectLocale() {
	if (!browser) return defaultLocale;

	// Check localStorage first
	const stored = localStorage.getItem('locale');
	if (stored && supportedLocales.includes(stored)) {
		return stored;
	}

	// Check browser language
	const navigatorLanguages = navigator.languages || [navigator.language];
	
	for (const lang of navigatorLanguages) {
		// Check exact match first
		if (supportedLocales.includes(lang)) {
			return lang;
		}
		
		// Check language code only (e.g., 'en' from 'en-US')
		const langCode = lang.split('-')[0];
		if (supportedLocales.includes(langCode)) {
			return langCode;
		}
	}

	return defaultLocale;
}

// Initialize i18n
init({
	fallbackLocale: defaultLocale,
	initialLocale: detectLocale(),
	loadingDelay: 200,
	formats: {
		number: {
			currency: { style: 'currency', currency: 'USD', minimumFractionDigits: 2 },
			percent: { style: 'percent', minimumFractionDigits: 0 },
			decimal: { style: 'decimal', minimumFractionDigits: 0 }
		},
		date: {
			short: { month: 'short', day: 'numeric', year: 'numeric' },
			long: { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' },
			time: { hour: 'numeric', minute: 'numeric' },
			datetime: { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric' }
		}
	}
});

export { supportedLocales, defaultLocale, detectLocale };