<script>
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { auth } from '$lib/stores/auth';
	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import toast, { Toaster } from 'svelte-french-toast';
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { init, waitLocale } from 'svelte-i18n';
	import { setLocale } from '$lib/i18n/utils.js';
	import { currentLocale, isLocaleInitialized } from '$lib/stores/i18n.js';
	import '$lib/i18n/index.js'; // Initialize i18n
	
	let { data, children } = $props();
	
	// Initialize i18n on component mount
	onMount(async () => {
		if (browser && data.locale) {
			try {
				// Set initial locale
				setLocale(data.locale);
				
				// Wait for locale to be fully loaded
				await waitLocale(data.locale);
				
				// Mark as initialized
				isLocaleInitialized.set(true);
			} catch (error) {
				console.error('Error initializing i18n:', error);
				// Fallback to English if there's an error
				setLocale('en');
				isLocaleInitialized.set(true);
			}
		}
	});
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="min-h-screen bg-white">
	<Header />
	<main>
		{@render children?.()}
	</main>
	
	<Footer />
</div>
  
  <Toaster 
    position="top-right" 
    toastOptions={{
      duration: 4000,
      style: 'border-radius: 8px; font-size: 14px;',
      success: {
        iconTheme: {
          primary: '#10b981',
          secondary: '#ffffff'
        }
      },
      error: {
        iconTheme: {
          primary: '#ef4444',
          secondary: '#ffffff'
        }
      }
    }}
  />