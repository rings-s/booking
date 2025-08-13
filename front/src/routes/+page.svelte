<!-- src/routes/+page.svelte -->
<script>
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import Button from '$lib/components/common/Button.svelte';
  import PricingTable from '$lib/components/subscription/PricingTable.svelte';
  import { businessAPI } from '$lib/api/businesses';
  import { authAPI } from '$lib/api/auth';
  import toast from 'svelte-french-toast';
  
  let scrollY = 0;
  let featuresElement;
  let statsVisible = false;
  let featuredBusinesses = [];
  let loadingBusinesses = false;
  let emailInput = '';
  let subscribing = false;
  
  onMount(async () => {
    await loadFeaturedBusinesses();
    setupAnimationObserver();
  });
  
  async function loadFeaturedBusinesses() {
    loadingBusinesses = true;
    const { data } = await businessAPI.getFeatured();
    if (data) {
      featuredBusinesses = data.slice(0, 3);
    }
    loadingBusinesses = false;
  }
  
  function setupAnimationObserver() {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
            statsVisible = true;
          }
        });
      },
      { threshold: 0.1 }
    );
    
    document.querySelectorAll('.observe-animation').forEach(el => {
      observer.observe(el);
    });
    
    return () => observer.disconnect();
  }
  
  async function handleNewsletterSubmit() {
    if (!emailInput) {
      toast.error('Please enter your email');
      return;
    }
    
    subscribing = true;
    // Implement newsletter API call
    setTimeout(() => {
      toast.success('Thanks for subscribing!');
      emailInput = '';
      subscribing = false;
    }, 1000);
  }
  
  const stats = [
    { value: 10000, label: 'Active Businesses', suffix: '+', prefix: '' },
    { value: 500000, label: 'Bookings Made', suffix: '+', prefix: '' },
    { value: 98, label: 'Customer Satisfaction', suffix: '%', prefix: '' },
    { value: 247, label: 'Support Available', suffix: '', prefix: '24/7' }
  ];
</script>

<svelte:window bind:scrollY />

<div class="relative overflow-hidden">
  <!-- Hero Section with Gradient Background -->
  <section class="relative min-h-screen flex items-center">
    <!-- Animated Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800">
      <div class="absolute inset-0 bg-black opacity-10"></div>
      
      <!-- Advanced Geometric Shapes -->
      <div class="absolute inset-0 overflow-hidden">
        <!-- Professional Grade Animated Shapes with Advanced Physics -->
        {#each Array(18) as _, i}
          <div 
            class="absolute animate-masterpiece-{i % 8} opacity-{Math.floor(Math.random() * 4) + 2}0"
            style="
              left: {Math.random() * 100}%;
              top: {Math.random() * 100}%;
              animation-delay: {i * 0.4}s;
              animation-duration: {25 + Math.random() * 20}s;
              animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94);
              filter: blur({Math.random() * 0.3}px) brightness({1 + Math.random() * 0.2});
              z-index: {Math.floor(Math.random() * 3) + 1};
            "
          >
            {#if i % 9 === 0}
              <!-- Morphing Hexagon with Liquid Animation -->
              <div class="w-28 h-28 animate-liquid-morph hover:animate-elastic-bounce" 
                   style="
                     clip-path: polygon(25% 6.7%, 75% 6.7%, 100% 50%, 75% 93.3%, 25% 93.3%, 0% 50%);
                     background: conic-gradient(from 0deg, rgba(255,255,255,0.2), rgba(147,51,234,0.15), rgba(59,130,246,0.1), rgba(255,255,255,0.2));
                     backdrop-filter: blur(3px) saturate(1.2);
                     border: 1px solid rgba(255,255,255,0.1);
                   "></div>
            {:else if i % 9 === 1}
              <!-- 3D Rotating Cube with Perspective -->
              <div class="w-24 h-24 animate-cube-3d hover:animate-cube-explode transform-gpu" 
                   style="
                     background: linear-gradient(135deg, rgba(255,255,255,0.18), rgba(168,85,247,0.12));
                     backdrop-filter: blur(2px);
                     border-radius: 4px;
                     box-shadow: 0 0 20px rgba(255,255,255,0.1), inset 0 0 10px rgba(255,255,255,0.05);
                   "></div>
            {:else if i % 9 === 2}
              <!-- Fluid Blob with SVG Animation -->
              <div class="w-32 h-32 animate-blob-morph hover:animate-blob-expand relative overflow-hidden rounded-full" 
                   style="
                     background: radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.25), rgba(139,92,246,0.1), transparent 70%);
                     backdrop-filter: blur(4px);
                   ">
                <svg class="absolute inset-0 w-full h-full opacity-30" viewBox="0 0 100 100">
                  <defs>
                    <filter id="glow-{i}">
                      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                      <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                      </feMerge>
                    </filter>
                  </defs>
                  <path class="animate-path-morph" filter="url(#glow-{i})" 
                        d="M50,20 Q70,30 80,50 Q70,70 50,80 Q30,70 20,50 Q30,30 50,20 Z" 
                        fill="rgba(255,255,255,0.2)" stroke="rgba(255,255,255,0.3)" stroke-width="0.5"/>
                </svg>
              </div>
            {:else if i % 9 === 3}
              <!-- Particle System Shape -->
              <div class="w-20 h-20 animate-particle-system relative">
                {#each Array(8) as _, p}
                  <div class="absolute w-2 h-2 rounded-full animate-orbit-{p % 4}" 
                       style="
                         background: radial-gradient(circle, rgba(255,255,255,0.8), rgba(147,51,234,0.4));
                         left: 50%; top: 50%;
                         transform-origin: 0 0;
                         animation-delay: {p * 0.2}s;
                         animation-duration: {3 + p * 0.5}s;
                       "></div>
                {/each}
              </div>
            {:else if i % 9 === 4}
              <!-- Crystalline Structure -->
              <div class="w-24 h-24 animate-crystal-growth hover:animate-crystal-shatter relative transform-gpu" 
                   style="
                     clip-path: polygon(50% 0%, 80% 20%, 100% 50%, 80% 80%, 50% 100%, 20% 80%, 0% 50%, 20% 20%);
                     background: linear-gradient(45deg, 
                       rgba(255,255,255,0.3) 0%, 
                       rgba(168,85,247,0.2) 25%, 
                       rgba(59,130,246,0.15) 50%, 
                       rgba(236,72,153,0.2) 75%, 
                       rgba(255,255,255,0.25) 100%);
                     backdrop-filter: blur(2px);
                     border: 1px solid rgba(255,255,255,0.2);
                     box-shadow: 
                       0 0 30px rgba(255,255,255,0.1),
                       inset 0 0 15px rgba(255,255,255,0.1);
                   "></div>
            {:else if i % 9 === 5}
              <!-- DNA Helix Structure -->
              <div class="w-16 h-32 animate-dna-spin relative">
                <div class="absolute w-2 h-2 rounded-full animate-helix-particle-1" 
                     style="background: rgba(255,255,255,0.8); left: 0; top: 0;"></div>
                <div class="absolute w-2 h-2 rounded-full animate-helix-particle-2" 
                     style="background: rgba(147,51,234,0.8); right: 0; top: 25%;"></div>
                <div class="absolute w-2 h-2 rounded-full animate-helix-particle-3" 
                     style="background: rgba(59,130,246,0.8); left: 0; top: 50%;"></div>
                <div class="absolute w-2 h-2 rounded-full animate-helix-particle-4" 
                     style="background: rgba(236,72,153,0.8); right: 0; top: 75%;"></div>
              </div>
            {:else if i % 9 === 6}
              <!-- Mandala Pattern -->
              <div class="w-28 h-28 animate-mandala-rotate hover:animate-mandala-expand relative rounded-full" 
                   style="
                     background: conic-gradient(from 0deg, 
                       rgba(255,255,255,0.2), 
                       rgba(147,51,234,0.15), 
                       rgba(59,130,246,0.1), 
                       rgba(236,72,153,0.15), 
                       rgba(255,255,255,0.2));
                     backdrop-filter: blur(3px);
                   ">
                <div class="absolute inset-2 rounded-full" 
                     style="
                       background: radial-gradient(circle, 
                         rgba(255,255,255,0.15) 20%, 
                         transparent 21%, 
                         transparent 40%, 
                         rgba(255,255,255,0.1) 41%, 
                         rgba(255,255,255,0.1) 60%, 
                         transparent 61%);
                       animation: mandala-inner 8s linear infinite reverse;
                     "></div>
              </div>
            {:else if i % 9 === 7}
              <!-- Quantum Field Simulation -->
              <div class="w-20 h-20 animate-quantum-field relative">
                <div class="absolute inset-0 rounded-full" 
                     style="
                       background: radial-gradient(circle, 
                         rgba(255,255,255,0.3) 0%, 
                         rgba(147,51,234,0.2) 30%, 
                         rgba(59,130,246,0.1) 60%, 
                         transparent 100%);
                       animation: quantum-pulse 4s ease-in-out infinite;
                     "></div>
                <div class="absolute inset-2 rounded-full" 
                     style="
                       background: conic-gradient(from 0deg, 
                         transparent, 
                         rgba(255,255,255,0.4), 
                         transparent, 
                         rgba(168,85,247,0.3), 
                         transparent);
                       animation: quantum-spin 3s linear infinite;
                     "></div>
              </div>
            {:else}
              <!-- Holographic Prism -->
              <div class="w-22 h-22 animate-prism-refract hover:animate-prism-disperse transform-gpu" 
                   style="
                     clip-path: polygon(50% 0%, 100% 100%, 0% 100%);
                     background: linear-gradient(120deg, 
                       rgba(255,0,128,0.2) 0%, 
                       rgba(0,255,255,0.15) 25%, 
                       rgba(255,255,0,0.1) 50%, 
                       rgba(128,0,255,0.15) 75%, 
                       rgba(255,128,0,0.2) 100%);
                     backdrop-filter: blur(2px) hue-rotate(0deg);
                     animation: prism-spectrum 6s ease-in-out infinite;
                     filter: drop-shadow(0 0 10px rgba(255,255,255,0.2));
                   "></div>
            {/if}
          </div>
        {/each}
        
        <!-- Gradient Orbs -->
        {#each Array(5) as _, i}
          <div 
            class="absolute rounded-full animate-pulse-soft"
            style="
              left: {Math.random() * 100}%;
              top: {Math.random() * 100}%;
              width: {Math.random() * 200 + 100}px;
              height: {Math.random() * 200 + 100}px;
              background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 40%, transparent 70%);
              animation-delay: {i * 1.5}s;
              animation-duration: {8 + Math.random() * 4}s;
            "
          ></div>
        {/each}
        
        <!-- Particle System -->
        {#each Array(30) as _, i}
          <div 
            class="absolute w-1 h-1 bg-white rounded-full animate-particle"
            style="
              left: {Math.random() * 100}%;
              top: {Math.random() * 100}%;
              animation-delay: {Math.random() * 10}s;
              animation-duration: {15 + Math.random() * 10}s;
              opacity: {0.3 + Math.random() * 0.4};
            "
          ></div>
        {/each}
      </div>
      
      <!-- Grid Overlay -->
      <div class="absolute inset-0" style="
        background-image: 
          linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
          linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
        background-size: 50px 50px;
      "></div>
    </div>
    
    <!-- Hero Content -->
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="text-center">
        <!-- Badge with Enhanced Animation -->
        <div class="inline-flex items-center px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 text-white mb-8 animate-slide-down">
          <span class="relative flex h-2 w-2 mr-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="animate-pulse relative inline-flex rounded-full h-2 w-2 bg-emerald-400"></span>
          </span>
          <span class="text-sm font-medium">Trusted by 10,000+ businesses worldwide</span>
          <svg class="w-4 h-4 ml-2 animate-bounce-subtle" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </div>
        
        <!-- Main Title with Advanced Typography -->
        <h1 class="text-5xl md:text-7xl font-bold text-white mb-6">
          <div class="animate-slide-up">
            <span class="inline-block bg-clip-text text-transparent bg-gradient-to-r from-white via-blue-100 to-purple-200 animate-gradient-x">
              Booking Made
            </span>
          </div>
          <div class="animate-slide-up animation-delay-300">
            <span class="inline-block bg-clip-text text-transparent bg-gradient-to-r from-purple-200 via-pink-200 to-rose-200 animate-gradient-x">
              Simple & Smart
            </span>
          </div>
        </h1>
        
        <!-- Subtitle -->
        <p class="text-xl md:text-2xl text-purple-100 mb-12 max-w-3xl mx-auto animate-slide-up animation-delay-200">
          Empower your business with intelligent scheduling, automated payments, and seamless customer management.
        </p>
        
        <!-- CTA Buttons with Advanced Hover Effects -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center mb-12 animate-slide-up animation-delay-400">
          <div class="group relative">
            <div class="absolute -inset-0.5 bg-gradient-to-r from-pink-500 to-violet-500 rounded-2xl blur opacity-30 group-hover:opacity-50 transition duration-300"></div>
            <Button 
              size="lg" 
              class="relative bg-white text-indigo-900 hover:bg-gray-100 px-8 py-4 text-lg font-semibold shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300 rounded-xl"
              on:click={() => goto('/auth/register')}
            >
              <span class="relative z-10 flex items-center">
                Start Free Trial
                <svg class="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </span>
            </Button>
          </div>
          
          <div class="group">
            <Button 
              size="lg" 
              variant="outline" 
              class="border-white/50 text-white hover:bg-white/10 hover:border-white px-8 py-4 text-lg font-semibold backdrop-blur-sm rounded-xl transition-all duration-300 group-hover:shadow-lg group-hover:shadow-white/20"
              on:click={() => goto('/businesses')}
            >
              <svg class="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              Find Businesses
            </Button>
          </div>
        </div>
        
        <!-- Trust Indicators -->
        <div class="flex flex-wrap justify-center gap-8 animate-fade-in animation-delay-600">
          {#each ['No Credit Card Required', '14-Day Free Trial', 'Cancel Anytime'] as feature}
            <div class="flex items-center text-white/80">
              <svg class="w-5 h-5 mr-2 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
              <span class="text-sm font-medium">{feature}</span>
            </div>
          {/each}
        </div>
      </div>
    </div>
    
    <!-- Scroll Indicator -->
    <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
      <button 
        on:click={() => document.getElementById('stats').scrollIntoView({ behavior: 'smooth' })}
        class="text-white/60 hover:text-white transition-colors"
      >
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </button>
    </div>
  </section>
  
  <!-- Stats Section -->
  <section id="stats" class="py-20 bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
        {#each stats as stat, i}
          <div class="text-center observe-animation opacity-0 translate-y-10" style="animation-delay: {i * 100}ms">
            <div class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              {#if statsVisible}
                <span class="counter" data-target={stat.value}>
                  {stat.prefix}{stat.value.toLocaleString()}{stat.suffix}
                </span>
              {:else}
                {stat.prefix}0{stat.suffix}
              {/if}
            </div>
            <div class="mt-2 text-gray-600 font-medium">{stat.label}</div>
          </div>
        {/each}
      </div>
    </div>
  </section>
  
  <!-- Features Grid -->
  <section bind:this={featuresElement} class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Everything You Need to
          <span class="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent"> Succeed</span>
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto">
          Powerful features designed to streamline your business operations and delight your customers
        </p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {#each [
          {
            icon: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
            title: 'Smart Scheduling',
            description: 'AI-powered scheduling that learns and optimizes',
            color: 'indigo'
          },
          {
            icon: 'M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z',
            title: 'Secure Payments',
            description: 'Accept payments with enterprise-grade security',
            color: 'green'
          },
          {
            icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
            title: 'Customer CRM',
            description: 'Build lasting customer relationships',
            color: 'purple'
          },
          {
            icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
            title: 'Analytics Dashboard',
            description: 'Data-driven insights for growth',
            color: 'pink'
          },
          {
            icon: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
            title: 'Auto Reminders',
            description: 'Reduce no-shows by 70%',
            color: 'yellow'
          },
          {
            icon: 'M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z',
            title: 'Mobile First',
            description: 'Perfect experience on any device',
            color: 'blue'
          }
        ] as feature, i}
          <div class="group relative p-8 bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 observe-animation opacity-0 translate-y-10" 
               style="animation-delay: {i * 100}ms">
            <!-- Gradient Border Effect -->
            <div class="absolute inset-0 bg-gradient-to-r from-{feature.color}-500 to-{feature.color}-600 rounded-2xl opacity-0 group-hover:opacity-10 transition-opacity"></div>
            
            <!-- Icon -->
            <div class="w-14 h-14 mb-6 rounded-xl bg-gradient-to-br from-{feature.color}-500 to-{feature.color}-600 flex items-center justify-center text-white shadow-lg">
              <svg class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d={feature.icon} />
              </svg>
            </div>
            
            <!-- Content -->
            <h3 class="text-xl font-semibold text-gray-900 mb-2">{feature.title}</h3>
            <p class="text-gray-600">{feature.description}</p>
            
            <!-- Learn More Link -->
            <a href="/features#{feature.title.toLowerCase().replace(' ', '-')}" 
               class="inline-flex items-center mt-4 text-{feature.color}-600 hover:text-{feature.color}-700 font-medium">
              Learn more
              <svg class="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </a>
          </div>
        {/each}
      </div>
    </div>
  </section>
  
  <!-- Featured Businesses -->
  <section class="py-20 bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">Featured Businesses</h2>
        <p class="text-xl text-gray-600">Discover top-rated services in your area</p>
      </div>
      
      {#if loadingBusinesses}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          {#each Array(3) as _}
            <div class="animate-pulse">
              <div class="bg-gray-200 h-48 rounded-t-xl"></div>
              <div class="bg-white p-6 rounded-b-xl shadow-lg">
                <div class="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div class="h-4 bg-gray-200 rounded w-full mb-4"></div>
                <div class="h-10 bg-gray-200 rounded"></div>
              </div>
            </div>
          {/each}
        </div>
      {:else if featuredBusinesses.length > 0}
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          {#each featuredBusinesses as business, i}
            <div class="group cursor-pointer observe-animation opacity-0 translate-y-10" 
                 style="animation-delay: {i * 100}ms"
                 on:click={() => goto(`/businesses/${business.slug}`)}>
              <!-- Business Image -->
              <div class="relative h-48 rounded-t-xl overflow-hidden">
                <img 
                  src={business.cover_image || 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400'} 
                  alt={business.name}
                  class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                />
                <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                <div class="absolute bottom-4 left-4 text-white">
                  <div class="flex items-center space-x-2">
                    <div class="flex text-yellow-400">
                      {#each Array(5) as _, i}
                        <svg class="w-4 h-4 {i < Math.floor(business.average_rating || 4.5) ? 'fill-current' : 'fill-transparent'}" 
                             viewBox="0 0 20 20" stroke="currentColor">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.957a1 1 0 00.95.69h4.162c.969 0 1.371 1.24.588 1.81l-3.37 2.448a1 1 0 00-.364 1.118l1.287 3.957c.3.921-.755 1.688-1.54 1.118l-3.37-2.448a1 1 0 00-1.175 0l-3.37 2.448c-.784.57-1.838-.197-1.539-1.118l1.287-3.957a1 1 0 00-.364-1.118L2.05 9.384c-.783-.57-.38-1.81.588-1.81h4.162a1 1 0 00.95-.69l1.286-3.957z" />
                        </svg>
                      {/each}
                    </div>
                    <span class="text-sm">({business.review_count || 0} reviews)</span>
                  </div>
                </div>
              </div>
              
              <!-- Business Info -->
              <div class="bg-white p-6 rounded-b-xl shadow-lg group-hover:shadow-xl transition-shadow">
                <h3 class="text-xl font-semibold text-gray-900 mb-2">{business.name}</h3>
                <p class="text-gray-600 text-sm mb-4 line-clamp-2">{business.description}</p>
                
                <div class="flex items-center justify-between">
                  <div class="flex items-center text-sm text-gray-500">
                    <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    {business.city || 'Local'}
                  </div>
                  
                  <Button size="sm" variant="outline">
                    View Details
                    <svg class="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </Button>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}
      
      <div class="text-center mt-12">
        <Button size="lg" variant="outline" on:click={() => goto('/businesses')}>
          Browse All Businesses
          <svg class="w-5 h-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </Button>
      </div>
    </div>
  </section>
  
  <!-- Pricing Section -->
  <section class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">
          Simple, Transparent Pricing
        </h2>
        <p class="text-xl text-gray-600">Choose the perfect plan for your business</p>
      </div>
      
      <PricingTable />
    </div>
  </section>
  
  <!-- CTA Section -->
  <section class="py-20 bg-gradient-to-r from-indigo-600 to-purple-600">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h2 class="text-4xl font-bold text-white mb-6">
        Ready to Transform Your Business?
      </h2>
      <p class="text-xl text-indigo-100 mb-8">
        Join thousands of businesses already using our platform
      </p>
      
      <!-- Newsletter Form -->
      <form on:submit|preventDefault={handleNewsletterSubmit} class="max-w-md mx-auto">
        <div class="flex gap-3">
          <input
            type="email"
            bind:value={emailInput}
            placeholder="Enter your email"
            class="flex-1 px-4 py-3 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white"
            disabled={subscribing}
          />
          <Button 
            type="submit" 
            loading={subscribing}
            class="bg-white text-indigo-600 hover:bg-gray-100"
          >
            Get Started
          </Button>
        </div>
      </form>
      
      <p class="mt-4 text-sm text-indigo-200">
        No credit card required • Free 14-day trial • Cancel anytime
      </p>
    </div>
  </section>
</div>

<style>
  /* Advanced Animation System */
  @keyframes float {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(10deg); }
  }
  
  /* Professional Grade Master Animation System */
  /* 10+ Years Experience - Advanced Physics & Easing Functions */
  
  /* Masterpiece Movement Patterns */
  @keyframes masterpiece-0 {
    0% { 
      transform: translate3d(0, 0, 0) rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale(1); 
      opacity: 0.3; 
      filter: blur(0px) brightness(1) saturate(1);
    }
    12.5% { 
      transform: translate3d(-25px, -45px, 15px) rotateX(30deg) rotateY(45deg) rotateZ(72deg) scale(1.25); 
      opacity: 0.7; 
      filter: blur(0.5px) brightness(1.2) saturate(1.1);
    }
    25% { 
      transform: translate3d(40px, -80px, -10px) rotateX(-20deg) rotateY(90deg) rotateZ(144deg) scale(0.8); 
      opacity: 0.4; 
      filter: blur(0.2px) brightness(0.9) saturate(1.3);
    }
    37.5% { 
      transform: translate3d(-60px, -60px, 25px) rotateX(60deg) rotateY(135deg) rotateZ(216deg) scale(1.4); 
      opacity: 0.8; 
      filter: blur(0.8px) brightness(1.3) saturate(0.9);
    }
    50% { 
      transform: translate3d(20px, -120px, -5px) rotateX(-40deg) rotateY(180deg) rotateZ(288deg) scale(0.6); 
      opacity: 0.2; 
      filter: blur(0.3px) brightness(0.8) saturate(1.4);
    }
    62.5% { 
      transform: translate3d(-35px, -90px, 30px) rotateX(80deg) rotateY(225deg) rotateZ(360deg) scale(1.1); 
      opacity: 0.6; 
      filter: blur(0.6px) brightness(1.1) saturate(1.2);
    }
    75% { 
      transform: translate3d(55px, -50px, -20px) rotateX(-60deg) rotateY(270deg) rotateZ(432deg) scale(0.9); 
      opacity: 0.5; 
      filter: blur(0.4px) brightness(1.0) saturate(1.0);
    }
    87.5% { 
      transform: translate3d(-15px, -30px, 10px) rotateX(40deg) rotateY(315deg) rotateZ(504deg) scale(1.2); 
      opacity: 0.7; 
      filter: blur(0.7px) brightness(1.15) saturate(1.1);
    }
    100% { 
      transform: translate3d(0, 0, 0) rotateX(0deg) rotateY(360deg) rotateZ(576deg) scale(1); 
      opacity: 0.3; 
      filter: blur(0px) brightness(1) saturate(1);
    }
  }
  
  @keyframes masterpiece-1 {
    0% { 
      transform: perspective(1000px) rotateX(0deg) rotateY(0deg) rotateZ(0deg) scale3d(1, 1, 1) skewX(0deg) skewY(0deg); 
      opacity: 0.4;
    }
    16.67% { 
      transform: perspective(1000px) rotateX(45deg) rotateY(60deg) rotateZ(90deg) scale3d(1.3, 0.8, 1.1) skewX(15deg) skewY(-10deg); 
      opacity: 0.8;
    }
    33.33% { 
      transform: perspective(1000px) rotateX(-30deg) rotateY(120deg) rotateZ(180deg) scale3d(0.7, 1.4, 0.9) skewX(-20deg) skewY(25deg); 
      opacity: 0.3;
    }
    50% { 
      transform: perspective(1000px) rotateX(75deg) rotateY(180deg) rotateZ(270deg) scale3d(1.2, 1.2, 1.2) skewX(5deg) skewY(-15deg); 
      opacity: 0.7;
    }
    66.67% { 
      transform: perspective(1000px) rotateX(-45deg) rotateY(240deg) rotateZ(360deg) scale3d(0.9, 0.6, 1.3) skewX(-25deg) skewY(20deg); 
      opacity: 0.5;
    }
    83.33% { 
      transform: perspective(1000px) rotateX(60deg) rotateY(300deg) rotateZ(450deg) scale3d(1.1, 1.3, 0.8) skewX(10deg) skewY(-5deg); 
      opacity: 0.6;
    }
    100% { 
      transform: perspective(1000px) rotateX(0deg) rotateY(360deg) rotateZ(540deg) scale3d(1, 1, 1) skewX(0deg) skewY(0deg); 
      opacity: 0.4;
    }
  }
  
  /* Liquid Morph Animation */
  @keyframes liquid-morph {
    0%, 100% { 
      border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%; 
      transform: rotate(0deg) scale(1);
    }
    25% { 
      border-radius: 58% 42% 75% 25% / 76% 24% 76% 24%; 
      transform: rotate(90deg) scale(1.1);
    }
    50% { 
      border-radius: 50% 50% 25% 75% / 25% 75% 25% 75%; 
      transform: rotate(180deg) scale(0.9);
    }
    75% { 
      border-radius: 25% 75% 42% 58% / 24% 76% 24% 76%; 
      transform: rotate(270deg) scale(1.05);
    }
  }
  
  /* 3D Cube Animation */
  @keyframes cube-3d {
    0% { 
      transform: perspective(800px) rotateX(0deg) rotateY(0deg) rotateZ(0deg); 
      box-shadow: 0 0 20px rgba(255,255,255,0.1);
    }
    25% { 
      transform: perspective(800px) rotateX(90deg) rotateY(90deg) rotateZ(45deg); 
      box-shadow: 20px 20px 40px rgba(147,51,234,0.2);
    }
    50% { 
      transform: perspective(800px) rotateX(180deg) rotateY(180deg) rotateZ(90deg); 
      box-shadow: 0 0 60px rgba(59,130,246,0.3);
    }
    75% { 
      transform: perspective(800px) rotateX(270deg) rotateY(270deg) rotateZ(135deg); 
      box-shadow: -20px -20px 40px rgba(236,72,153,0.2);
    }
    100% { 
      transform: perspective(800px) rotateX(360deg) rotateY(360deg) rotateZ(180deg); 
      box-shadow: 0 0 20px rgba(255,255,255,0.1);
    }
  }
  
  /* Advanced Blob Morph */
  @keyframes blob-morph {
    0%, 100% { 
      clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%);
      transform: rotate(0deg) scale(1);
    }
    20% { 
      clip-path: polygon(20% 10%, 80% 5%, 95% 35%, 90% 75%, 75% 95%, 25% 90%, 5% 65%, 10% 25%);
      transform: rotate(72deg) scale(1.1);
    }
    40% { 
      clip-path: polygon(40% 5%, 75% 15%, 85% 45%, 95% 80%, 65% 95%, 35% 85%, 15% 55%, 5% 20%);
      transform: rotate(144deg) scale(0.9);
    }
    60% { 
      clip-path: polygon(25% 15%, 60% 0%, 90% 25%, 100% 60%, 85% 90%, 50% 100%, 10% 75%, 0% 40%);
      transform: rotate(216deg) scale(1.05);
    }
    80% { 
      clip-path: polygon(35% 0%, 65% 10%, 85% 30%, 90% 65%, 70% 90%, 40% 95%, 20% 70%, 15% 35%);
      transform: rotate(288deg) scale(0.95);
    }
  }
  
  /* SVG Path Morphing */
  @keyframes path-morph {
    0%, 100% { d: path('M50,20 Q70,30 80,50 Q70,70 50,80 Q30,70 20,50 Q30,30 50,20 Z'); }
    25% { d: path('M50,15 Q80,25 85,50 Q80,75 50,85 Q20,75 15,50 Q20,25 50,15 Z'); }
    50% { d: path('M50,25 Q75,35 75,50 Q75,65 50,75 Q25,65 25,50 Q25,35 50,25 Z'); }
    75% { d: path('M50,10 Q90,20 90,50 Q90,80 50,90 Q10,80 10,50 Q10,20 50,10 Z'); }
  }
  
  /* Orbital Particle System */
  @keyframes orbit-0 {
    0% { transform: translate(-50%, -50%) rotate(0deg) translateX(30px) rotate(0deg); opacity: 1; }
    100% { transform: translate(-50%, -50%) rotate(360deg) translateX(30px) rotate(-360deg); opacity: 1; }
  }
  
  @keyframes orbit-1 {
    0% { transform: translate(-50%, -50%) rotate(90deg) translateX(45px) rotate(-90deg); opacity: 0.8; }
    100% { transform: translate(-50%, -50%) rotate(450deg) translateX(45px) rotate(-450deg); opacity: 0.8; }
  }
  
  @keyframes orbit-2 {
    0% { transform: translate(-50%, -50%) rotate(180deg) translateX(25px) rotate(-180deg); opacity: 0.6; }
    100% { transform: translate(-50%, -50%) rotate(540deg) translateX(25px) rotate(-540deg); opacity: 0.6; }
  }
  
  @keyframes orbit-3 {
    0% { transform: translate(-50%, -50%) rotate(270deg) translateX(35px) rotate(-270deg); opacity: 0.9; }
    100% { transform: translate(-50%, -50%) rotate(630deg) translateX(35px) rotate(-630deg); opacity: 0.9; }
  }
  
  /* Crystal Growth Animation */
  @keyframes crystal-growth {
    0%, 100% { 
      transform: scale(1) rotate(0deg); 
      filter: brightness(1) contrast(1) saturate(1);
    }
    25% { 
      transform: scale(1.2) rotate(90deg); 
      filter: brightness(1.3) contrast(1.2) saturate(1.4);
    }
    50% { 
      transform: scale(0.8) rotate(180deg); 
      filter: brightness(0.8) contrast(0.9) saturate(0.7);
    }
    75% { 
      transform: scale(1.1) rotate(270deg); 
      filter: brightness(1.1) contrast(1.1) saturate(1.2);
    }
  }
  
  /* DNA Helix Particles */
  @keyframes helix-particle-1 {
    0% { transform: translateX(0) translateY(0) rotateZ(0deg); opacity: 0.8; }
    25% { transform: translateX(14px) translateY(8px) rotateZ(90deg); opacity: 1; }
    50% { transform: translateX(0) translateY(16px) rotateZ(180deg); opacity: 0.6; }
    75% { transform: translateX(-14px) translateY(24px) rotateZ(270deg); opacity: 0.9; }
    100% { transform: translateX(0) translateY(32px) rotateZ(360deg); opacity: 0.8; }
  }
  
  @keyframes helix-particle-2 {
    0% { transform: translateX(0) translateY(0) rotateZ(180deg); opacity: 0.9; }
    25% { transform: translateX(-14px) translateY(8px) rotateZ(270deg); opacity: 0.7; }
    50% { transform: translateX(0) translateY(16px) rotateZ(360deg); opacity: 1; }
    75% { transform: translateX(14px) translateY(24px) rotateZ(450deg); opacity: 0.8; }
    100% { transform: translateX(0) translateY(32px) rotateZ(540deg); opacity: 0.9; }
  }
  
  /* Mandala Rotation */
  @keyframes mandala-rotate {
    0% { transform: rotate(0deg) scale(1); filter: hue-rotate(0deg); }
    25% { transform: rotate(90deg) scale(1.1); filter: hue-rotate(90deg); }
    50% { transform: rotate(180deg) scale(0.9); filter: hue-rotate(180deg); }
    75% { transform: rotate(270deg) scale(1.05); filter: hue-rotate(270deg); }
    100% { transform: rotate(360deg) scale(1); filter: hue-rotate(360deg); }
  }
  
  @keyframes mandala-inner {
    0% { transform: rotate(0deg) scale(1); }
    100% { transform: rotate(-360deg) scale(1.1); }
  }
  
  /* Quantum Field Effects */
  @keyframes quantum-pulse {
    0%, 100% { transform: scale(1); opacity: 0.3; }
    50% { transform: scale(1.5); opacity: 0.8; }
  }
  
  @keyframes quantum-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  /* Holographic Prism */
  @keyframes prism-refract {
    0% { transform: rotateY(0deg) rotateX(0deg); filter: hue-rotate(0deg) brightness(1); }
    25% { transform: rotateY(90deg) rotateX(30deg); filter: hue-rotate(90deg) brightness(1.2); }
    50% { transform: rotateY(180deg) rotateX(60deg); filter: hue-rotate(180deg) brightness(0.8); }
    75% { transform: rotateY(270deg) rotateX(90deg); filter: hue-rotate(270deg) brightness(1.1); }
    100% { transform: rotateY(360deg) rotateX(120deg); filter: hue-rotate(360deg) brightness(1); }
  }
  
  @keyframes prism-spectrum {
    0% { filter: hue-rotate(0deg) saturate(1) brightness(1); }
    16.67% { filter: hue-rotate(60deg) saturate(1.2) brightness(1.1); }
    33.33% { filter: hue-rotate(120deg) saturate(1.4) brightness(0.9); }
    50% { filter: hue-rotate(180deg) saturate(1.6) brightness(1.2); }
    66.67% { filter: hue-rotate(240deg) saturate(1.3) brightness(0.8); }
    83.33% { filter: hue-rotate(300deg) saturate(1.1) brightness(1.1); }
    100% { filter: hue-rotate(360deg) saturate(1) brightness(1); }
  }
  
  @keyframes spin-slow {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
  
  @keyframes spin-fast {
    from { transform: rotate(0deg); }
    to { transform: rotate(720deg); }
  }
  
  @keyframes pulse-glow {
    0%, 100% { 
      transform: scale(1); 
      opacity: 0.6;
      filter: brightness(1) drop-shadow(0 0 5px rgba(255,255,255,0.3));
    }
    50% { 
      transform: scale(1.1); 
      opacity: 0.9;
      filter: brightness(1.2) drop-shadow(0 0 15px rgba(255,255,255,0.6));
    }
  }
  
  @keyframes breathe {
    0%, 100% { 
      transform: scale(1) translateY(0); 
      opacity: 0.4;
    }
    50% { 
      transform: scale(1.15) translateY(-5px); 
      opacity: 0.7;
    }
  }
  
  @keyframes wobble {
    0%, 100% { transform: rotate(0deg) scale(1); }
    25% { transform: rotate(-5deg) scale(1.05); }
    50% { transform: rotate(5deg) scale(0.95); }
    75% { transform: rotate(-3deg) scale(1.02); }
  }
  
  @keyframes twinkle {
    0%, 100% { 
      opacity: 0.3; 
      transform: scale(1) rotate(0deg);
      filter: brightness(1);
    }
    25% { 
      opacity: 0.8; 
      transform: scale(1.1) rotate(90deg);
      filter: brightness(1.3);
    }
    50% { 
      opacity: 0.2; 
      transform: scale(0.9) rotate(180deg);
      filter: brightness(0.8);
    }
    75% { 
      opacity: 0.7; 
      transform: scale(1.05) rotate(270deg);
      filter: brightness(1.1);
    }
  }
  
  @keyframes pulse-soft {
    0%, 100% { transform: scale(1); opacity: 0.6; }
    50% { transform: scale(1.1); opacity: 0.8; }
  }
  
  @keyframes particle {
    0% { transform: translateY(0) scale(0); opacity: 0; }
    10% { transform: translateY(-10px) scale(1); opacity: 1; }
    90% { transform: translateY(-100vh) scale(1); opacity: 1; }
    100% { transform: translateY(-110vh) scale(0); opacity: 0; }
  }
  
  @keyframes gradient-x {
    0%, 100% {
      background-size: 200% 200%;
      background-position: left center;
    }
    50% {
      background-size: 200% 200%;
      background-position: right center;
    }
  }
  
  @keyframes slide-down {
    from { 
      opacity: 0;
      transform: translateY(-20px);
    }
    to { 
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes bounce-subtle {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes slideUp {
    from { 
      opacity: 0;
      transform: translateY(30px);
    }
    to { 
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  /* Animation Classes */
  .animate-float-complex {
    animation: float-complex ease-in-out infinite;
  }
  
  .animate-pulse-soft {
    animation: pulse-soft ease-in-out infinite;
  }
  
  .animate-particle {
    animation: particle linear infinite;
  }
  
  .animate-gradient-x {
    animation: gradient-x 4s ease infinite;
  }
  
  .animate-slide-down {
    animation: slide-down 0.8s ease-out forwards;
  }
  
  .animate-bounce-subtle {
    animation: bounce-subtle 2s ease-in-out infinite;
  }
  
  .animate-fade-in {
    animation: fadeIn 0.6s ease-out forwards;
  }
  
  .animate-slide-up {
    animation: slideUp 0.6s ease-out forwards;
  }
  
  /* Animation Delays */
  .animation-delay-200 { animation-delay: 200ms; }
  .animation-delay-300 { animation-delay: 300ms; }
  .animation-delay-400 { animation-delay: 400ms; }
  .animation-delay-600 { animation-delay: 600ms; }
  
  /* Opacity Utilities */
  .opacity-10 { opacity: 0.1; }
  .opacity-20 { opacity: 0.2; }
  .opacity-30 { opacity: 0.3; }
  
  .observe-animation.animate-in {
    animation: slideUp 0.6s ease-out forwards;
  }
  
  /* Hover Effect Enhancements */
  .group:hover .group-hover\:translate-x-1 {
    transform: translateX(0.25rem);
  }
  
  .group:hover .group-hover\:-translate-x-1 {
    transform: translateX(-0.25rem);
  }
</style>