<!-- src/lib/components/layout/Header.svelte -->
<script>
    import { page } from '$app/stores';
    import { auth, isAuthenticated, currentUser, canManageBusinesses, isAdmin } from '$lib/stores/auth';
    import NotificationBell from './NotificationBell.svelte';
    import Button from '../common/Button.svelte';
    import LanguageSwitcher from '../common/LanguageSwitcher.svelte';
    import { t } from '$lib/stores/i18n.js';
    
    let mobileMenuOpen = $state(false);
    
    let currentPath = $derived($page.url.pathname);
    
    let navigation = $derived([
      { name: $t('common.home'), href: '/', show: 'always' },
      { name: $t('navigation.businesses'), href: '/businesses', show: 'always' },
      { name: $t('navigation.dashboard'), href: '/dashboard', show: 'authenticated' },
      { name: $t('navigation.bookings'), href: '/bookings', show: 'authenticated' },
      { name: $t('navigation.manage_businesses'), href: '/businesses/new', show: $canManageBusinesses ? 'authenticated' : 'never' }
    ]);
    
    function toggleMobileMenu() {
      mobileMenuOpen = !mobileMenuOpen;
    }
  </script>
  
  <header class="bg-white shadow-sm">
    <nav class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 justify-between">
        <div class="flex">
          <div class="flex flex-shrink-0 items-center">
            <a href="/" class="text-2xl font-bold text-blue-600">
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
                      ? 'border-b-2 border-blue-500 text-gray-900'
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
          <!-- Language Switcher -->
          <LanguageSwitcher variant="dropdown" />
          
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
            
            <Button variant="outline" size="sm" onclick={() => auth.logout()}>
              {$t('auth.logout')}
            </Button>
          {:else}
            <Button href="/auth/login" variant="outline" size="sm">
              {$t('auth.login')}
            </Button>
            <Button href="/auth/register" size="sm">
              {$t('auth.register')}
            </Button>
          {/if}
        </div>
        
        <div class="-mr-2 flex items-center sm:hidden">
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            onclick={toggleMobileMenu}
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
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-700'
                }"
                onclick={() => mobileMenuOpen = false}
              >
                {item.name}
              </a>
            {/if}
          {/each}
          
          <!-- Language switcher for mobile -->
          <div class="border-t border-gray-200 px-4 py-3">
            <div class="text-sm font-medium text-gray-500 mb-2">{$t('common.language')}</div>
            <LanguageSwitcher variant="select" showFlags={true} />
          </div>
          
          <!-- Auth buttons for mobile -->
          <div class="border-t border-gray-200 px-4 py-3 space-y-2">
            {#if $isAuthenticated}
              <Button 
                variant="outline" 
                size="sm" 
                class="w-full" 
                onclick={() => { auth.logout(); mobileMenuOpen = false; }}
              >
                {$t('auth.logout')}
              </Button>
            {:else}
              <Button href="/auth/login" variant="outline" size="sm" class="w-full">
                {$t('auth.login')}
              </Button>
              <Button href="/auth/register" size="sm" class="w-full">
                {$t('auth.register')}
              </Button>
            {/if}
          </div>
        </div>
      </div>
    {/if}
  </header>