<!-- src/lib/components/layout/Header.svelte -->
<script>
    import { page } from '$app/stores';
    import { auth, isAuthenticated, currentUser, canManageBusinesses, isAdmin } from '$lib/stores/auth';
    import NotificationBell from './NotificationBell.svelte';
    import Button from '../common/Button.svelte';
    
    let mobileMenuOpen = false;
    
    $: currentPath = $page.url.pathname;
    
    $: navigation = [
      { name: 'Home', href: '/', show: 'always' },
      { name: 'Businesses', href: '/businesses', show: 'always' },
      { name: 'Dashboard', href: '/dashboard', show: 'authenticated' },
      { name: 'My Bookings', href: '/bookings', show: 'authenticated' },
      { name: 'Manage Businesses', href: '/businesses/new', show: $canManageBusinesses ? 'authenticated' : 'never' }
    ];
    
    function toggleMobileMenu() {
      mobileMenuOpen = !mobileMenuOpen;
    }
  </script>
  
  <header class="bg-white shadow-sm">
    <nav class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 justify-between">
        <div class="flex">
          <div class="flex flex-shrink-0 items-center">
            <a href="/" class="text-2xl font-bold text-indigo-600">
              BookingPro
            </a>
          </div>
          
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            {#each navigation as item}
              {#if item.show === 'always' || (item.show === 'authenticated' && $isAuthenticated)}
                <a
                  href={item.href}
                  class="inline-flex items-center px-1 pt-1 text-sm font-medium {
                    currentPath === item.href
                      ? 'border-b-2 border-indigo-500 text-gray-900'
                      : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }"
                >
                  {item.name}
                </a>
              {/if}
            {/each}
          </div>
        </div>
        
        <div class="hidden sm:ml-6 sm:flex sm:items-center space-x-4">
          {#if $isAuthenticated}
            <NotificationBell />
            
            <div class="relative ml-3">
              <button
                type="button"
                class="flex rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                <span class="sr-only">Open user menu</span>
                <div class="h-8 w-8 rounded-full bg-indigo-600 flex items-center justify-center text-white">
                  {$currentUser?.first_name?.[0] || 'U'}
                </div>
              </button>
            </div>
            
            <Button variant="outline" size="sm" on:click={() => auth.logout()}>
              Logout
            </Button>
          {:else}
            <Button href="/auth/login" variant="outline" size="sm">
              Login
            </Button>
            <Button href="/auth/register" size="sm">
              Sign Up
            </Button>
          {/if}
        </div>
        
        <div class="-mr-2 flex items-center sm:hidden">
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
            on:click={toggleMobileMenu}
          >
            <span class="sr-only">Open main menu</span>
            {#if mobileMenuOpen}
              <svg class="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            {:else}
              <svg class="block h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            {/if}
          </button>
        </div>
      </div>
    </nav>
    
    {#if mobileMenuOpen}
      <div class="sm:hidden">
        <div class="space-y-1 pb-3 pt-2">
          {#each navigation as item}
            {#if item.show === 'always' || (item.show === 'authenticated' && $isAuthenticated)}
              <a
                href={item.href}
                class="block border-l-4 py-2 pl-3 pr-4 text-base font-medium {
                  currentPath === item.href
                    ? 'border-indigo-500 bg-indigo-50 text-indigo-700'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700'
                }"
                on:click={() => mobileMenuOpen = false}
              >
                {item.name}
              </a>
            {/if}
          {/each}
        </div>
      </div>
    {/if}
  </header>