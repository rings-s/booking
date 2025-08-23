<!-- src/lib/components/layout/Header.svelte -->
<script>
    import { page } from '$app/stores';
    import { auth, isAuthenticated, currentUser, canManageBusinesses, isAdmin } from '$lib/stores/auth';
    import NotificationBell from './NotificationBell.svelte';
    import Button from '../common/Button.svelte';
    import LanguageSwitcher from '../common/LanguageSwitcher.svelte';
    import { t } from '$lib/stores/i18n.js';
    
    let mobileMenuOpen = $state(false);
    let userMenuOpen = $state(false);
    let scrolled = $state(false);
    let mounted = $state(false);
    
    let currentPath = $derived($page.url.pathname);
    
    let navigation = $derived([
      { 
        name: $t('common.home'), 
        href: '/', 
        show: 'always',
        icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6'
      },
      { 
        name: $t('navigation.businesses'), 
        href: '/businesses', 
        show: 'always',
        icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4'
      },
      { 
        name: $t('navigation.dashboard'), 
        href: '/dashboard', 
        show: 'authenticated',
        icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
      },
      { 
        name: $t('navigation.bookings'), 
        href: '/bookings', 
        show: 'authenticated',
        icon: 'M8 7V3a1 1 0 011-1h6a1 1 0 011 1v4m4 0H4m16 0v10a2 2 0 01-2 2H6a2 2 0 01-2-2V7m16 0H4m0 0l2 2m14-2l-2 2'
      }
    ]);

    let dashboardMenuItems = $derived([
      { name: 'Overview', href: '/dashboard', icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z' },
      { name: 'My Bookings', href: '/bookings', icon: 'M8 7V3a1 1 0 011-1h6a1 1 0 011 1v4' },
      { name: 'Businesses', href: '/businesses', icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16' },
      { name: 'Analytics', href: '/dashboard/analytics', icon: 'M9 19v-6a2 2 0 00-2-2H5' },
      { name: 'Settings', href: '/dashboard/settings', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' }
    ]);
    
    // Effects for premium interactions
    $effect(() => {
      if (typeof window !== 'undefined') {
        mounted = true;
        
        const handleScroll = () => {
          scrolled = window.scrollY > 20;
        };
        
        const handleClickOutside = (event) => {
          if (userMenuOpen && !event.target.closest('.user-menu')) {
            userMenuOpen = false;
          }
        };
        
        window.addEventListener('scroll', handleScroll);
        document.addEventListener('click', handleClickOutside);
        
        return () => {
          window.removeEventListener('scroll', handleScroll);
          document.removeEventListener('click', handleClickOutside);
        };
      }
    });
    
    function toggleMobileMenu() {
      mobileMenuOpen = !mobileMenuOpen;
      if (mobileMenuOpen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    }
    
    function toggleUserMenu() {
      userMenuOpen = !userMenuOpen;
    }
    
    function closeMenus() {
      mobileMenuOpen = false;
      userMenuOpen = false;
      document.body.style.overflow = '';
    }
</script>
  
<!-- Premium Glassmorphic Navigation -->
<header 
  class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 ease-out "
  class:scrolled-nav={scrolled}
  class:mounted-nav={mounted}
>
  <nav class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="nav-container flex h-20 items-center justify-between">
      
      <!-- Animated Logo -->
      <div class="flex flex-shrink-0 items-center">
        <a 
          href="/" 
          class="logo-container group relative"
          onclick={closeMenus}
        >
          <div class="logo-bg absolute inset-0 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 opacity-0 group-hover:opacity-100 transition-all duration-300 blur-lg scale-110"></div>
          <div class="logo-text relative text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent group-hover:scale-105 transition-transform duration-300">
            BookingPro
          </div>
        </a>
      </div>
      
      <!-- Desktop Navigation Pills -->
      <div class="hidden lg:flex lg:items-center lg:space-x-2">
        {#each navigation as item, index}
          {#if item.show === 'always' || (item.show === 'authenticated' && $isAuthenticated)}
            <a
              href={item.href}
              class="nav-pill group relative flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 hover:scale-105"
              class:active-pill={currentPath === item.href}
              style="animation-delay: {index * 0.1}s"
              onclick={closeMenus}
            >
              <!-- Icon -->
              <svg class="w-4 h-4 transition-transform duration-300 group-hover:scale-110" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={item.icon} />
              </svg>
              
              <!-- Text -->
              <span class="relative z-10">{item.name}</span>
              
              <!-- Active indicator -->
              {#if currentPath === item.href}
                <div class="active-indicator absolute inset-0 rounded-full"></div>
              {/if}
              
              <!-- Hover effect -->
              <div class="hover-effect absolute inset-0 rounded-full opacity-0 group-hover:opacity-100 transition-all duration-300"></div>
            </a>
          {/if}
        {/each}
      </div>
      
      <!-- Desktop Right Section -->
      <div class="hidden lg:flex lg:items-center lg:space-x-3">
        <!-- Language Switcher -->
        <div class="nav-pill px-3 py-2 rounded-full">
          <LanguageSwitcher variant="dropdown" />
        </div>
        
        {#if $isAuthenticated}
          <!-- Notifications -->
          <div class="relative">
            <NotificationBell />
          </div>
          
          <!-- User Menu -->
          <div class="user-menu relative">
            <button
              type="button"
              class="user-avatar group flex items-center gap-3 rounded-full px-3 py-2 transition-all duration-300 hover:scale-105"
              onclick={toggleUserMenu}
            >
              <div class="avatar-container relative">
                <div class="avatar-ring absolute inset-0 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 opacity-0 group-hover:opacity-100 transition-all duration-300 blur-sm scale-110"></div>
                <div class="avatar-image relative h-8 w-8 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center text-white font-semibold text-sm group-hover:scale-105 transition-transform duration-300">
                  {$currentUser?.first_name?.[0] || 'U'}
                </div>
              </div>
              
              <div class="user-info hidden md:block text-left">
                <div class="text-sm font-medium text-gray-900">{$currentUser?.first_name || 'User'}</div>
                <div class="text-xs text-gray-500">{$currentUser?.email}</div>
              </div>
              
              <svg 
                class="w-4 h-4 text-gray-400 transition-transform duration-300"
                class:rotate-180={userMenuOpen}
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            <!-- User Dropdown -->
            {#if userMenuOpen}
              <div class="user-dropdown absolute right-0 top-full mt-2 w-72 origin-top-right">
                <div class="dropdown-container rounded-2xl shadow-2xl ring-1 ring-black ring-opacity-5">
                  <!-- User Info Header -->
                  <div class="dropdown-header p-4 border-b border-white/10">
                    <div class="flex items-center gap-3">
                      <div class="h-12 w-12 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center text-white font-bold">
                        {$currentUser?.first_name?.[0] || 'U'}
                      </div>
                      <div>
                        <div class="text-base font-semibold text-white">{$currentUser?.first_name} {$currentUser?.last_name}</div>
                        <div class="text-sm text-white/70">{$currentUser?.email}</div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Dashboard Menu Items -->
                  <div class="dropdown-menu p-2">
                    {#each dashboardMenuItems as menuItem, index}
                      <a
                        href={menuItem.href}
                        class="dropdown-item group flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-300 hover:scale-105"
                        style="animation-delay: {index * 0.05}s"
                        onclick={closeMenus}
                      >
                        <svg class="w-4 h-4 transition-transform duration-300 group-hover:scale-110" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={menuItem.icon} />
                        </svg>
                        <span>{menuItem.name}</span>
                      </a>
                    {/each}
                    
                    <div class="border-t border-white/10 mt-2 pt-2">
                      <button
                        class="dropdown-item group flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium w-full text-left transition-all duration-300 hover:scale-105"
                        onclick={() => { auth.logout(); closeMenus(); }}
                      >
                        <svg class="w-4 h-4 transition-transform duration-300 group-hover:scale-110" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                        </svg>
                        <span>{$t('auth.logout')}</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            {/if}
          </div>
        {:else}
          <!-- Auth Buttons -->
          <div class="flex items-center gap-3">
            <Button href="/auth/login" variant="outline" size="sm" class="nav-button">
              {$t('auth.login')}
            </Button>
            <Button href="/auth/register" size="sm" class="nav-button nav-button-primary">
              {$t('auth.register')}
            </Button>
          </div>
        {/if}
      </div>
      
      <!-- Mobile Menu Button -->
      <div class="lg:hidden">
        <button
          type="button"
          class="mobile-menu-button p-3 rounded-full transition-all duration-300 hover:scale-110"
          onclick={toggleMobileMenu}
          aria-label="Toggle menu"
        >
          <div class="hamburger-icon">
            <span class="hamburger-line" class:open={mobileMenuOpen}></span>
            <span class="hamburger-line" class:open={mobileMenuOpen}></span>
            <span class="hamburger-line" class:open={mobileMenuOpen}></span>
          </div>
        </button>
      </div>
    </div>
  </nav>
</header>

<!-- Mobile Menu Overlay -->
{#if mobileMenuOpen}
  <div class="mobile-overlay fixed inset-0 z-40 lg:hidden">
    <div class="mobile-backdrop absolute inset-0" onclick={toggleMobileMenu}></div>
    
    <div class="mobile-menu absolute right-0 top-0 h-full w-80 max-w-[85vw] sm:w-96 md:w-80">
      <div class="mobile-menu-content h-full overflow-y-auto">
        <!-- Mobile Header -->
        <div class="mobile-header p-6 border-b border-white/10">
          <div class="flex items-center justify-between">
            <div class="logo-text text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              BookingPro
            </div>
            <button 
              class="mobile-close-button p-2 rounded-full transition-all duration-300"
              onclick={toggleMobileMenu}
            >
              <svg class="w-6 h-6 text-white/70" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Mobile Navigation -->
        <div class="mobile-nav p-6 space-y-2">
          {#each navigation as item, index}
            {#if item.show === 'always' || (item.show === 'authenticated' && $isAuthenticated)}
              <a
                href={item.href}
                class="mobile-nav-item group flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 hover:scale-105"
                class:active={currentPath === item.href}
                style="animation-delay: {index * 0.1}s"
                onclick={toggleMobileMenu}
              >
                <svg class="w-5 h-5 transition-transform duration-300 group-hover:scale-110" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={item.icon} />
                </svg>
                <span class="font-medium">{item.name}</span>
              </a>
            {/if}
          {/each}
        </div>
        
        <!-- Mobile User Section -->
        {#if $isAuthenticated}
          <div class="mobile-user-section border-t border-white/10 p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="h-12 w-12 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center text-white font-bold">
                {$currentUser?.first_name?.[0] || 'U'}
              </div>
              <div>
                <div class="text-base font-semibold text-white">{$currentUser?.first_name}</div>
                <div class="text-sm text-white/70">{$currentUser?.email}</div>
              </div>
            </div>
            
            <div class="space-y-2">
              {#each dashboardMenuItems as menuItem, index}
                <a
                  href={menuItem.href}
                  class="mobile-nav-item group flex items-center gap-3 px-3 py-2 rounded-lg transition-all duration-300"
                  style="animation-delay: {index * 0.05}s"
                  onclick={toggleMobileMenu}
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={menuItem.icon} />
                  </svg>
                  <span class="text-sm">{menuItem.name}</span>
                </a>
              {/each}
              
              <button
                class="mobile-nav-item group flex items-center gap-3 px-3 py-2 rounded-lg w-full text-left transition-all duration-300"
                onclick={() => { auth.logout(); toggleMobileMenu(); }}
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013 3v1" />
                </svg>
                <span class="text-sm">{$t('auth.logout')}</span>
              </button>
            </div>
          </div>
        {:else}
          <div class="mobile-auth-section border-t border-white/10 p-6 space-y-3">
            <Button href="/auth/login" variant="outline" size="md" class="w-full" onclick={toggleMobileMenu}>
              {$t('auth.login')}
            </Button>
            <Button href="/auth/register" size="md" class="w-full" onclick={toggleMobileMenu}>
              {$t('auth.register')}
            </Button>
          </div>
        {/if}
        
        <!-- Language Switcher -->
        <div class="mobile-language-section border-t border-white/10 p-6">
          <div class="text-sm font-medium text-white/70 mb-3">{$t('common.language')}</div>
          <LanguageSwitcher variant="select" showFlags={true} />
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  /* Premium Navigation Styles */
  header {
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.8);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 
      0 1px 3px rgba(0, 0, 0, 0.1),
      0 1px 2px rgba(0, 0, 0, 0.06),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  header.scrolled-nav {
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 
      0 4px 20px rgba(0, 0, 0, 0.1),
      0 1px 3px rgba(0, 0, 0, 0.08),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  header.mounted-nav {
    animation: nav-slide-down 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }

  @keyframes nav-slide-down {
    0% {
      transform: translateY(-100%);
      opacity: 0;
    }
    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }

  /* Navigation Container */
  .nav-container {
    position: relative;
    transition: all 0.3s ease;
  }

  /* Logo Styles */
  .logo-container {
    padding: 0.5rem;
    border-radius: 0.75rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .logo-container:hover {
    transform: translateY(-2px);
  }

  /* Navigation Pills */
  .nav-pill {
    position: relative;
    color: #6b7280;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    animation: nav-item-fade-in 0.6s ease-out both;
  }

  .nav-pill:hover {
    color: #4f46e5;
    background: rgba(79, 70, 229, 0.1);
    border-color: rgba(79, 70, 229, 0.3);
    box-shadow: 
      0 4px 20px rgba(79, 70, 229, 0.15),
      0 0 0 1px rgba(79, 70, 229, 0.1);
  }

  .nav-pill.active-pill {
    color: #4f46e5;
    background: rgba(79, 70, 229, 0.15);
    border-color: rgba(79, 70, 229, 0.3);
    font-weight: 600;
  }

  .active-indicator {
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.2), rgba(139, 92, 246, 0.2));
    border: 1px solid rgba(79, 70, 229, 0.3);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .hover-effect {
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(139, 92, 246, 0.1));
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  @keyframes nav-item-fade-in {
    0% {
      opacity: 0;
      transform: translateY(-10px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* User Avatar */
  .user-avatar {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  .user-avatar:hover {
    background: rgba(79, 70, 229, 0.1);
    border-color: rgba(79, 70, 229, 0.3);
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.15);
  }

  /* User Dropdown */
  .user-dropdown {
    animation: dropdown-fade-in 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 60;
  }

  .dropdown-container {
    background: rgba(30, 41, 59, 0.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 
      0 25px 50px -12px rgba(0, 0, 0, 0.5),
      0 0 0 1px rgba(255, 255, 255, 0.05),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .dropdown-item {
    color: rgba(255, 255, 255, 0.8);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: dropdown-item-fade-in 0.4s ease-out both;
  }

  .dropdown-item:hover {
    color: white;
    background: rgba(79, 70, 229, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  @keyframes dropdown-fade-in {
    0% {
      opacity: 0;
      transform: scale(0.95) translateY(-10px);
    }
    100% {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }

  @keyframes dropdown-item-fade-in {
    0% {
      opacity: 0;
      transform: translateX(-10px);
    }
    100% {
      opacity: 1;
      transform: translateX(0);
    }
  }

  /* Mobile Menu Button */
  .mobile-menu-button {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  .mobile-menu-button:hover {
    background: rgba(79, 70, 229, 0.1);
    border-color: rgba(79, 70, 229, 0.3);
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.15);
  }

  /* Animated Hamburger */
  .hamburger-icon {
    width: 24px;
    height: 18px;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .hamburger-line {
    width: 100%;
    height: 2px;
    background: #6b7280;
    border-radius: 1px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    transform-origin: center;
  }

  .hamburger-line:nth-child(1).open {
    transform: translateY(8px) rotate(45deg);
  }

  .hamburger-line:nth-child(2).open {
    opacity: 0;
    transform: scaleX(0);
  }

  .hamburger-line:nth-child(3).open {
    transform: translateY(-8px) rotate(-45deg);
  }

  /* Mobile Overlay */
  .mobile-overlay {
    animation: overlay-fade-in 0.3s ease-out;
  }

  .mobile-backdrop {
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
  }

  .mobile-menu {
    animation: mobile-slide-in 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .mobile-menu-content {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.98), rgba(51, 65, 85, 0.98));
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 
      -10px 0 50px rgba(0, 0, 0, 0.3),
      inset 1px 0 0 rgba(255, 255, 255, 0.1);
  }

  .mobile-nav-item {
    color: rgba(255, 255, 255, 0.8);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: mobile-item-fade-in 0.5s ease-out both;
  }

  .mobile-nav-item:hover {
    color: white;
    background: rgba(79, 70, 229, 0.2);
    border-color: rgba(79, 70, 229, 0.3);
    transform: translateX(8px);
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.15);
  }

  .mobile-nav-item.active {
    color: white;
    background: rgba(79, 70, 229, 0.3);
    border-color: rgba(79, 70, 229, 0.5);
    font-weight: 600;
  }

  .mobile-close-button {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
  }

  .mobile-close-button:hover {
    background: rgba(239, 68, 68, 0.2);
    border-color: rgba(239, 68, 68, 0.3);
  }

  @keyframes overlay-fade-in {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }

  @keyframes mobile-slide-in {
    0% {
      transform: translateX(100%);
    }
    100% {
      transform: translateX(0);
    }
  }

  @keyframes mobile-item-fade-in {
    0% {
      opacity: 0;
      transform: translateX(20px);
    }
    100% {
      opacity: 1;
      transform: translateX(0);
    }
  }

  /* Navigation Buttons */
  .nav-button {
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .nav-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }

  .nav-button-primary {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
  }

  .nav-button-primary:hover {
    box-shadow: 0 8px 25px rgba(79, 70, 229, 0.4);
  }

  /* Performance optimizations */
  .nav-pill,
  .user-avatar,
  .mobile-menu-button,
  .mobile-nav-item,
  .dropdown-item {
    will-change: transform, background-color, border-color, box-shadow;
  }

  /* Responsive adjustments */
  @media (prefers-reduced-motion: reduce) {
    * {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }

  /* Extra large screens - Enhanced spacing */
  @media (min-width: 1536px) {
    .nav-container {
      padding: 0 3rem;
    }
    
    .nav-pill {
      padding: 0.75rem 1.5rem;
    }
  }

  /* Large screens - Standard desktop */
  @media (max-width: 1024px) {
    .nav-pill {
      padding: 0.5rem 1rem;
      font-size: 0.875rem;
    }
    
    .logo-text {
      font-size: 1.5rem;
    }
  }

  /* Medium screens - Tablet landscape */
  @media (max-width: 768px) {
    header {
      padding: 0.25rem 0;
    }

    .nav-container {
      height: 4rem;
      padding: 0 1rem;
    }
    
    .logo-text {
      font-size: 1.25rem;
    }
    
    .mobile-menu {
      width: 100vw;
      max-width: 100vw;
    }
  }

  /* Small screens - Mobile portrait */
  @media (max-width: 640px) {
    .nav-container {
      height: 3.5rem;
      padding: 0 0.75rem;
    }
    
    .logo-text {
      font-size: 1.125rem;
    }
    
    .mobile-menu-content {
      padding: 1rem;
    }
    
    .mobile-header {
      padding: 1rem;
    }
    
    .mobile-nav {
      padding: 1rem;
    }
  }

  /* Extra small screens - Compact mobile */
  @media (max-width: 480px) {
    .nav-container {
      height: 3rem;
      padding: 0 0.5rem;
    }
    
    .logo-text {
      font-size: 1rem;
    }
    
    .mobile-menu-button {
      padding: 0.5rem;
    }
    
    .hamburger-icon {
      width: 20px;
      height: 15px;
    }
  }

  /* Touch device optimizations */
  @media (hover: none) and (pointer: coarse) {
    .nav-pill,
    .user-avatar,
    .mobile-nav-item,
    .dropdown-item {
      min-height: 44px; /* iOS/Android minimum touch target */
    }
    
    /* Reduce hover effects on touch devices */
    .nav-pill:hover,
    .user-avatar:hover,
    .mobile-menu-button:hover {
      transform: none;
    }
  }

  /* High DPI displays */
  @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
    .hamburger-line {
      height: 2px;
    }
    
    header {
      border-bottom-width: 0.5px;
    }
  }
</style>