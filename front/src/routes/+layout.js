// src/routes/+layout.js
import { browser } from '$app/environment';
import { auth } from '$lib/stores/auth';
import { googleAuth } from '$lib/utils/google-auth';

export async function load({ fetch, data }) {
  // Initialize auth store and preload Google auth on client side
  if (browser) {
    // Initialize auth store
    await auth.init();
    
    // Preload Google authentication script for faster login
    try {
      await googleAuth.initialize();
    } catch (error) {
      console.warn('Failed to preload Google auth:', error);
    }
  }
  
  return {
    ...data
  };
}