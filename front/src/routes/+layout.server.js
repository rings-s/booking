// src/routes/+layout.server.js

export async function load({ locals }) {
  // Pass the detected locale from hooks.server.js to the client
  return {
    locale: locals.locale || 'en'
  };
}