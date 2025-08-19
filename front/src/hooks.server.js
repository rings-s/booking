// src/hooks.server.js
import { PUBLIC_API_URL } from '$env/static/public';

export async function handle({ event, resolve }) {
  // Detect locale from headers
  const acceptLanguage = event.request.headers.get('accept-language');
  const supportedLocales = ['en', 'es', 'fr', 'de', 'ar'];
  const defaultLocale = 'en';
  
  let detectedLocale = defaultLocale;
  
  // Check URL path for locale (e.g., /es/dashboard)
  const pathLocale = event.url.pathname.split('/')[1];
  if (supportedLocales.includes(pathLocale)) {
    detectedLocale = pathLocale;
  } 
  // Check cookie for stored locale preference
  else if (event.cookies.get('locale') && supportedLocales.includes(event.cookies.get('locale'))) {
    detectedLocale = event.cookies.get('locale');
  }
  // Parse Accept-Language header
  else if (acceptLanguage) {
    const languages = acceptLanguage
      .split(',')
      .map(lang => lang.trim().split(';')[0])
      .map(lang => lang.split('-')[0]); // Extract language code only
    
    detectedLocale = languages.find(lang => supportedLocales.includes(lang)) || defaultLocale;
  }
  
  // Store detected locale in event.locals for use in load functions
  event.locals.locale = detectedLocale;

  // Pass cookies to API requests on server side
  event.locals.fetch = async (url, options = {}) => {
    if (url.startsWith('/api/') || url.startsWith(PUBLIC_API_URL)) {
      options.headers = {
        ...options.headers,
        cookie: event.request.headers.get('cookie') || ''
      };
    }
    return fetch(url, options);
  };

  // Parse JWT from cookies if present
  const token = event.cookies.get('access_token');
  if (token) {
    event.locals.token = token;
    try {
      // Decode JWT to get user info (without verification for performance)
      const base64Payload = token.split('.')[1];
      const payload = JSON.parse(atob(base64Payload));
      event.locals.user = payload.user;
    } catch (error) {
      event.locals.user = null;
    }
  }

  const response = await resolve(event, {
    transformPageChunk: ({ html }) => {
      // Set lang and dir attributes on html element for SSR
      const isRTL = detectedLocale === 'ar';
      return html
        .replace('<html lang="en">', `<html lang="${detectedLocale}" dir="${isRTL ? 'rtl' : 'ltr'}">`)
        .replace('%sveltekit.head%', `%sveltekit.head%<script>window.__INITIAL_LOCALE__ = '${detectedLocale}';</script>`);
    }
  });
  
  return response;
}

export async function handleFetch({ request, fetch }) {
  return fetch(request);
}