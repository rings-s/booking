// src/hooks.server.js
import { PUBLIC_API_URL } from '$env/static/public';

export async function handle({ event, resolve }) {
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

  const response = await resolve(event);
  return response;
}

export async function handleFetch({ request, fetch }) {
  return fetch(request);
}