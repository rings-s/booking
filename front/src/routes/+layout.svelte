<script>
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { auth } from '$lib/stores/auth';
	import Header from '$lib/components/layout/Header.svelte';
	import Footer from '$lib/components/layout/Footer.svelte';
	import toast, { Toaster } from 'svelte-french-toast';
	
	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="min-h-screen bg-gray-50">
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