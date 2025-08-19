// src/routes/+layout.js
import { browser } from '$app/environment';
import { auth } from '$lib/stores/auth';
import { googleAuth } from '$lib/utils/google-auth';
import { getCurrentUserSSR } from '$lib/api/auth';
import { init, waitLocale } from 'svelte-i18n';
import { detectLocale } from '$lib/i18n/index.js';

export async function load({ fetch, data, url }) {
  // Initialize i18n
  const initialLocale = browser 
    ? (window.__INITIAL_LOCALE__ || detectLocale()) 
    : data?.locale || 'en';

  // Initialize svelte-i18n
  if (!browser) {
    // Server-side initialization
    init({
      fallbackLocale: 'en',
      initialLocale: initialLocale
    });
  }

  // Wait for locale to load before continuing
  if (browser) {
    await waitLocale(initialLocale);
  }

  // Initialize auth store and preload Google auth on client side
  if (browser) {
    // Use SvelteKit fetch to get current user data
    const { data: userData } = await getCurrentUserSSR(fetch);
    
    // Initialize auth store with fetched user data
    auth.initWithUser(userData);
    
    // Preload Google authentication script for faster login
    try {
      await googleAuth.initialize();
    } catch (error) {
      console.warn('Failed to preload Google auth:', error);
    }
  } else {
    // Server-side: set auth to not loading
    auth.setLoading(false);
  }
  
  return {
    locale: initialLocale,
    ...data
  };
}