<!-- src/routes/+page.svelte -->
<script>
  import { goto } from '$app/navigation';
  import { fade, slide } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import Button from '$lib/components/common/Button.svelte';
  import { auth, isAuthenticated } from '$lib/stores/auth';
  import { businessAPI } from '$lib/api/businesses';
  import toast from 'svelte-french-toast';

  let emailInput = $state('');
  let subscribing = $state(false);
  let featuredBusinesses = $state([]);
  let loadingBusinesses = $state(false);
  
  // Premium hero state management
  let heroVisible = $state(false);
  let mousePosition = $state({ x: 0, y: 0 });
  let statsAnimated = $state(false);
  
  // Derived values for interactive effects
  let parallaxOffset = $derived(() => mousePosition.y * 0.02);
  let glowIntensity = $derived(() => mousePosition.x / (typeof window !== 'undefined' ? window.innerWidth : 1));

  // Load featured businesses on component initialization
  $effect(async () => {
    await loadFeaturedBusinesses();
  });

  // Hero interaction effects
  $effect(() => {
    const handleMouseMove = (e) => {
      mousePosition = { x: e.clientX, y: e.clientY };
    };

    const handleIntersection = (entries) => {
      entries.forEach(entry => {
        heroVisible = entry.isIntersecting;
        if (entry.isIntersecting && !statsAnimated) {
          setTimeout(() => { statsAnimated = true; }, 500);
        }
      });
    };

    if (typeof window !== 'undefined') {
      document.addEventListener('mousemove', handleMouseMove);
      
      const observer = new IntersectionObserver(handleIntersection, { threshold: 0.3 });
      const heroElement = document.querySelector('#premium-hero');
      if (heroElement) observer.observe(heroElement);

      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        observer.disconnect();
      };
    }
  });

  async function loadFeaturedBusinesses() {
    loadingBusinesses = true;
    const { data } = await businessAPI.getFeatured();
    if (data) {
      featuredBusinesses = data.slice(0, 3);
    }
    loadingBusinesses = false;
  }

  function handleGetStarted() {
    if ($isAuthenticated) {
      goto('/dashboard');
    } else {
      goto('/auth/register');
    }
  }

  async function handleNewsletterSubmit() {
    if (!emailInput.trim()) {
      toast.error('Please enter your email address');
      return;
    }

    subscribing = true;
    try {
      // Simulate newsletter signup
      await new Promise(resolve => setTimeout(resolve, 1000));
      toast.success('Thank you for subscribing!');
      emailInput = '';
    } catch (error) {
      toast.error('Failed to subscribe. Please try again.');
    } finally {
      subscribing = false;
    }
  }

  const features = [
    {
      icon: '📅',
      title: 'Easy Online Booking',
      description: 'Let customers book appointments 24/7 with your customizable booking page'
    },
    {
      icon: '⚡',
      title: 'Automated Reminders',
      description: 'Reduce no-shows with automatic email and SMS reminders'
    },
    {
      icon: '📊',
      title: 'Smart Analytics',
      description: 'Track your business performance with detailed reports and insights'
    },
    {
      icon: '💳',
      title: 'Secure Payments',
      description: 'Accept payments online with integrated payment processing'
    },
    {
      icon: '🔄',
      title: 'Real-time Sync',
      description: 'Sync with Google Calendar, Outlook, and other calendar apps'
    },
    {
      icon: '🎨',
      title: 'Custom Branding',
      description: 'Match your brand with customizable booking pages and forms'
    }
  ];

  const industries = [
    {
      name: 'Healthcare',
      icon: '🏥',
      description: 'Perfect for clinics, dentists, and medical practices'
    },
    {
      name: 'Beauty & Wellness',
      icon: '💇‍♀️',
      description: 'Ideal for salons, spas, and wellness centers'
    },
    {
      name: 'Fitness',
      icon: '🏃‍♂️',
      description: 'Great for gyms, trainers, and fitness studios'
    },
    {
      name: 'Education',
      icon: '🎓',
      description: 'Excellent for tutoring, courses, and training'
    }
  ];

  const testimonials = [
    {
      name: 'Sarah Johnson',
      business: 'Wellness Spa',
      text: 'BookingPro transformed our appointment system. We reduced no-shows by 40% and our staff loves how easy it is to use.',
      rating: 5
    },
    {
      name: 'Dr. Michael Chen',
      business: 'Chen Medical Clinic',
      text: 'The automated reminders and online booking have saved us countless hours. Our patients appreciate the convenience.',
      rating: 5
    },
    {
      name: 'Emma Rodriguez',
      business: 'FitLife Gym',
      text: 'Managing class bookings has never been easier. The real-time sync with our calendar is a game-changer.',
      rating: 5
    }
  ];

  const pricingPlans = [
    {
      name: 'Free',
      price: 0,
      description: 'Perfect for getting started',
      features: [
        '50 bookings/month',
        '1 business',
        '5 services',
        'Email notifications'
      ],
      variant: 'outline',
      popular: false
    },
    {
      name: 'Starter',
      price: 9,
      description: 'For small businesses',
      features: [
        '200 bookings/month',
        '2 businesses',
        '20 services total',
        'Email reminders'
      ],
      variant: 'outline',
      popular: false
    },
    {
      name: 'Professional',
      price: 29,
      description: 'For growing businesses',
      features: [
        '1,000 bookings/month',
        '5 businesses',
        'Unlimited services',
        'Analytics dashboard'
      ],
      variant: 'secondary',
      popular: true,
      bg: 'bg-blue-600 text-white border-blue-600',
      checkColor: 'text-green-400'
    },
    {
      name: 'Business',
      price: 79,
      description: 'For large businesses',
      features: [
        '5,000 bookings/month',
        'Unlimited businesses',
        'Custom branding',
        'Priority support'
      ],
      variant: 'outline',
      popular: false
    }
  ];
</script>

<svelte:head>
  <title>BookingPro - Online Appointment Scheduling Made Simple</title>
  <meta name="description" content="Streamline your business with our powerful online booking system. Free trial, no setup fees, and 24/7 customer support.">
</svelte:head>

<div class="min-h-screen bg-white">
  <!-- Premium Hero Section -->
  <section 
    id="premium-hero"
    class="relative min-h-screen flex items-center overflow-hidden"
    style="transform: translateY({parallaxOffset}px)"
  >
    <!-- Multi-layer Background System -->
    <div class="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900"></div>
    <div class="absolute inset-0 bg-gradient-to-tr from-blue-600/20 via-purple-600/30 to-pink-600/20"></div>
    <div class="absolute inset-0 bg-gradient-radial from-transparent via-indigo-500/10 to-transparent"></div>
    
    <!-- Animated Background Particles -->
    <div class="absolute inset-0 overflow-hidden">
      {#each Array(12) as _, i}
        <div 
          class="absolute w-1 h-1 bg-white/20 rounded-full animate-pulse"
          style="
            left: {20 + (i * 8)}%;
            top: {15 + (i * 6)}%;
            animation-delay: {i * 0.5}s;
            animation-duration: {3 + (i * 0.2)}s;
          "
        ></div>
      {/each}
    </div>

    <!-- Main Content Container -->
    <div class="@container/hero relative z-10 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid lg:grid-cols-12 gap-8 lg:gap-16 items-center min-h-screen py-20">
        
        <!-- Left Content Column -->
        <div class="lg:col-span-7 space-y-8">
          <!-- Main Headlines -->
          <div class="space-y-6" class:animate-fade-up={heroVisible}>
            <div class="inline-flex items-center px-4 py-2 rounded-full bg-white/10 backdrop-blur-sm border border-white/20 text-white/80 text-sm font-medium">
              ✨ Trusted by 10,000+ businesses worldwide
            </div>
            
            <h1 class="text-[clamp(3rem,8vw,6rem)] leading-[0.9] font-bold text-white tracking-tight">
              Transform Your
              <span class="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
                Booking Experience
              </span>
            </h1>
            
            <p class="text-xl lg:text-2xl text-white/70 leading-relaxed max-w-2xl">
              The most advanced appointment scheduling platform that grows with your business. 
              <span class="text-white/90 font-medium">Reduce no-shows by 65%</span> and automate your entire booking workflow.
            </p>
          </div>

          <!-- Premium CTA Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 pt-4">
            <Button 
              size="lg" 
              class="group relative px-8 py-4 text-lg font-semibold bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white border-0 shadow-2xl hover:shadow-blue-500/25 transition-all duration-300 transform hover:scale-105"
              style="box-shadow: 0 0 {Math.round(glowIntensity * 50)}px rgba(99, 102, 241, 0.3)"
              on:click={handleGetStarted}
            >
              <span class="relative z-10">Start Free Trial</span>
              <div class="absolute inset-0 bg-gradient-to-r from-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg"></div>
            </Button>
            
            <Button 
              variant="outline" 
              size="lg" 
              class="px-8  py-4 text-lg font-semibold border-white/30 text-white hover:bg-white/10 hover:border-white/50 backdrop-blur-sm transition-all duration-300"
              on:click={() => goto('/demo')}
            >
              Watch Demo →
            </Button>
          </div>

          <!-- Trust Indicators -->
          <div class="flex items-center gap-8 pt-6 text-white/60">
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              <span class="text-sm">Free 14-day trial</span>
            </div>
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              <span class="text-sm">No setup fees</span>
            </div>
            <div class="flex items-center gap-2">
              <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
              </svg>
              <span class="text-sm">Cancel anytime</span>
            </div>
          </div>
        </div>

        <!-- Right Visual Column -->
        <div class="lg:col-span-5 relative">
          <!-- Floating Glassmorphic Stats Cards -->
          <div class="relative z-10 space-y-4 lg:space-y-6">
            <!-- Main Dashboard Card -->
            <div 
              class="glassmorphic-card p-4 lg:p-6 rounded-2xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-2xl transform transition-all duration-500 hover:scale-105"
              class:animate-float-up={statsAnimated}
              role="button"
              tabindex="0"
              on:keydown={(e) => e.key === 'Enter' && (statsAnimated = !statsAnimated)}
            >
              <div class="flex items-center justify-between mb-3 lg:mb-4">
                <h3 class="text-white font-semibold text-sm lg:text-base">Today's Bookings</h3>
                <div class="w-2 h-2 lg:w-3 lg:h-3 bg-green-400 rounded-full animate-pulse"></div>
              </div>
              <div class="text-2xl lg:text-3xl font-bold text-white mb-1 lg:mb-2 tabular-nums">
                {statsAnimated ? '247' : '0'}
              </div>
              <div class="text-white/60 text-xs lg:text-sm">↗ 23% from yesterday</div>
            </div>

            <!-- Revenue Card -->
            <div 
              class="glassmorphic-card p-4 lg:p-6 rounded-2xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-2xl ml-4 lg:ml-8 transform transition-all duration-500 hover:scale-105"
              class:animate-float-up={statsAnimated}
              style="animation-delay: 0.2s"
              role="button"
              tabindex="0"
            >
              <div class="flex items-center justify-between mb-3 lg:mb-4">
                <h3 class="text-white font-semibold text-sm lg:text-base">Revenue</h3>
                <div class="text-xl lg:text-2xl">💰</div>
              </div>
              <div class="text-2xl lg:text-3xl font-bold text-white mb-1 lg:mb-2 tabular-nums">
                ${statsAnimated ? '12,847' : '0'}
              </div>
              <div class="text-white/60 text-xs lg:text-sm">This month</div>
            </div>

            <!-- Customer Satisfaction Card -->
            <div 
              class="glassmorphic-card p-4 lg:p-6 rounded-2xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-2xl transform transition-all duration-500 hover:scale-105"
              class:animate-float-up={statsAnimated}
              style="animation-delay: 0.4s"
              role="button"
              tabindex="0"
            >
              <div class="flex items-center justify-between mb-3 lg:mb-4">
                <h3 class="text-white font-semibold text-sm lg:text-base">Satisfaction</h3>
                <div class="flex space-x-0.5">
                  {#each Array(5) as _, i}
                    <span 
                      class="text-yellow-400 text-sm lg:text-base transition-all duration-300 hover:scale-125"
                      style="animation-delay: {i * 0.1}s"
                    >★</span>
                  {/each}
                </div>
              </div>
              <div class="text-2xl lg:text-3xl font-bold text-white mb-1 lg:mb-2 tabular-nums">
                {statsAnimated ? '4.9' : '0.0'}
              </div>
              <div class="text-white/60 text-xs lg:text-sm">Average rating</div>
            </div>

            <!-- Interactive Feature Highlights -->
            <div class="mt-6 lg:mt-8 space-y-3">
              <div class="flex items-center text-white/80 text-sm lg:text-base">
                <div class="w-2 h-2 bg-blue-400 rounded-full mr-3 animate-pulse"></div>
                <span>Real-time dashboard updates</span>
              </div>
              <div class="flex items-center text-white/80 text-sm lg:text-base">
                <div class="w-2 h-2 bg-purple-400 rounded-full mr-3 animate-pulse" style="animation-delay: 0.3s"></div>
                <span>Automated payment processing</span>
              </div>
              <div class="flex items-center text-white/80 text-sm lg:text-base">
                <div class="w-2 h-2 bg-pink-400 rounded-full mr-3 animate-pulse" style="animation-delay: 0.6s"></div>
                <span>Smart reminder system</span>
              </div>
            </div>
          </div>

          <!-- Enhanced Background Glow Effects -->
          <div class="absolute -top-10 -right-10 w-48 h-48 lg:w-72 lg:h-72 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
          <div class="absolute -bottom-10 -left-10 w-40 h-40 lg:w-64 lg:h-64 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s"></div>
          <div class="absolute top-1/2 -right-20 w-32 h-32 lg:w-48 lg:h-48 bg-pink-500/15 rounded-full blur-2xl animate-pulse" style="animation-delay: 2s"></div>
        </div>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16" in:fade={{ duration: 800 }}>
        <h2 class="text-3xl lg:text-4xl font-extrabold text-gray-900 mb-4">
          Everything you need to manage bookings
        </h2>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Our comprehensive platform adapts to how you do business, not the other way around.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {#each features as feature, index}
          <div 
            class="bg-white p-6 rounded-2xl border border-gray-200 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
            in:slide={{ delay: 100 * index, duration: 600, easing: quintOut }}
          >
            <div class="text-4xl mb-4 transform transition-transform duration-300 hover:scale-110">{feature.icon}</div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
            <p class="text-gray-600">{feature.description}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- Industries Section -->
  <section class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16" in:fade={{ duration: 800 }}>
        <h2 class="text-3xl lg:text-4xl font-extrabold text-gray-900 mb-4">
          Perfect for every industry
        </h2>
        <p class="text-xl text-gray-600">
          Join thousands of businesses already using BookingPro
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {#each industries as industry, index}
          <div 
            class="bg-white p-6 rounded-2xl text-center border border-gray-200 hover:shadow-md transition-all duration-300 transform hover:-translate-y-1"
            in:slide={{ delay: 100 * index, duration: 600, easing: quintOut }}
          >
            <div class="text-5xl mb-4 transform transition-transform duration-300 hover:rotate-12">{industry.icon}</div>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">{industry.name}</h3>
            <p class="text-gray-600 text-sm">{industry.description}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- Testimonials Section -->
  <section class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16" in:fade={{ duration: 800 }}>
        <h2 class="text-3xl lg:text-4xl font-extrabold text-gray-900 mb-4">
          Loved by businesses worldwide
        </h2>
        <p class="text-xl text-gray-600">
          See what our customers have to say
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        {#each testimonials as testimonial, index}
          <div 
            class="bg-gray-50 p-6 rounded-2xl border border-gray-200 hover:shadow-lg transition-all duration-300"
            in:fade={{ delay: 100 * index, duration: 600, opacity: 0 }}
          >
            <div class="flex mb-4">
              {#each Array(testimonial.rating) as _}
                <span class="text-yellow-400 text-xl mr-1 animate-pulse">★</span>
              {/each}
            </div>
            <blockquote class="text-gray-700 mb-4 italic">
              "{testimonial.text}"
            </blockquote>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3 shadow-sm">
                <span class="text-blue-600 font-semibold">{testimonial.name.charAt(0)}</span>
              </div>
              <div>
                <p class="font-semibold text-gray-900">{testimonial.name}</p>
                <p class="text-gray-600 text-sm">{testimonial.business}</p>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- Pricing Section -->
  <section class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16" in:fade={{ duration: 800 }}>
        <h2 class="text-3xl lg:text-4xl font-extrabold text-gray-900 mb-4">
          Simple, transparent pricing
        </h2>
        <p class="text-xl text-gray-600">
          Start free, upgrade as you grow. No hidden fees, cancel anytime.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {#each pricingPlans as plan, index}
          <div 
            class="bg-white p-6 rounded-2xl border-2 {plan.popular ? 'border-blue-600 shadow-xl scale-105' : 'border-gray-200'} relative overflow-hidden transition-all duration-300 hover:shadow-xl {plan.bg || ''}"
            in:slide={{ delay: 100 * index, duration: 600, easing: quintOut }}
          >
            {#if plan.popular}
              <div class="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                <span class="bg-yellow-400 text-black px-4 py-1 rounded-full text-sm font-semibold shadow-md">
                  Most Popular
                </span>
              </div>
            {/if}
            <div class="text-center">
              <h3 class="text-xl font-bold {plan.popular ? 'text-white' : 'text-gray-900'} mb-2">{plan.name}</h3>
              <div class="text-3xl font-bold {plan.popular ? 'text-white' : 'text-gray-900'} mb-2">${plan.price}</div>
              <p class="{plan.popular ? 'text-blue-100' : 'text-gray-600'} mb-6">{plan.description}</p>
            </div>
            <ul class="space-y-3 mb-8">
              {#each plan.features as feature}
                <li class="flex items-center {plan.popular ? 'text-white' : 'text-gray-700'}">
                  <svg class="w-5 h-5 {plan.checkColor || 'text-green-500'} mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  {feature}
                </li>
              {/each}
            </ul>
            <Button variant={plan.variant} fullWidth on:click={handleGetStarted} class="shadow-md hover:shadow-lg transition-shadow duration-300">
              Start Free Trial
            </Button>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="py-20 bg-gradient-to-r from-blue-600 to-indigo-600 text-white relative overflow-hidden">
    <div class="absolute inset-0 opacity-20" style="background-image: url('data:image/svg+xml,%3Csvg width=%22100%22 height=%22100%22 viewBox=%220 0 100 100%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cg stroke=%22%23FFF%22 stroke-width=%222%22 stroke-opacity=%220.5%22%3E%3Cpath d=%22M-10 50h120M50 -10v120%22/%3E%3C/g%3E%3C/svg%3E');"></div>
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10" in:fade={{ duration: 800 }}>
      <h2 class="text-3xl lg:text-4xl font-extrabold mb-6">
        Ready to streamline your bookings?
      </h2>
      <p class="text-xl text-blue-100 mb-8">
        Join thousands of businesses already using BookingPro to save time and grow their business.
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <Button 
          variant="secondary" 
          size="lg" 
          class="px-8 py-4 text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
          on:click={handleGetStarted}
        >
          Start Your Free Trial
        </Button>
        <p class="text-blue-100 text-sm">
          Free 14-day trial • No credit card required
        </p>
      </div>
    </div>
  </section>

  <!-- Newsletter Section -->
  <section class="py-16 bg-gray-50">
    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 text-center" in:fade={{ duration: 800 }}>
      <h3 class="text-2xl font-extrabold text-gray-900 mb-4">
        Stay updated with booking tips and updates
      </h3>
      <p class="text-gray-600 mb-6">
        Get the latest features, tips, and industry insights delivered to your inbox.
      </p>
      <form on:submit|preventDefault={handleNewsletterSubmit} class="flex flex-col sm:flex-row gap-3">
        <input
          type="email"
          bind:value={emailInput}
          placeholder="Enter your email address"
          class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
          required
        />
        <Button 
          type="submit" 
          disabled={subscribing}
          class="px-6 py-3 whitespace-nowrap shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105"
        >
          {subscribing ? 'Subscribing...' : 'Subscribe'}
        </Button>
      </form>
    </div>
  </section> 
</div>

<style>
  /* Premium Hero Animations & Effects */
  @keyframes float-up {
    0% {
      transform: translateY(30px);
      opacity: 0;
    }
    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }

  @keyframes fade-up {
    0% {
      transform: translateY(20px);
      opacity: 0;
    }
    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }

  @keyframes particle-float {
    0%, 100% {
      transform: translateY(0px) translateX(0px);
      opacity: 0.3;
    }
    50% {
      transform: translateY(-20px) translateX(10px);
      opacity: 0.6;
    }
  }

  .animate-float-up {
    animation: float-up 0.8s ease-out forwards;
  }

  .animate-fade-up {
    animation: fade-up 1s ease-out forwards;
  }

  .glassmorphic-card {
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
    will-change: transform;
  }

  .glassmorphic-card:hover {
    transform: translateY(-8px) scale(1.02);
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 
      0 25px 50px -12px rgba(0, 0, 0, 0.25),
      0 0 0 1px rgba(255, 255, 255, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  /* Custom Gradient Extensions */
  .bg-gradient-radial {
    background: radial-gradient(ellipse at center, var(--tw-gradient-stops));
  }

  /* Smooth transitions for all interactive elements */
  * {
    transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
    transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Advanced Button Glow Effect */
  .group:hover .glow-effect {
    box-shadow: 
      0 0 20px rgba(59, 130, 246, 0.5),
      0 0 40px rgba(59, 130, 246, 0.3),
      0 0 60px rgba(59, 130, 246, 0.1);
  }

  /* Responsive text scaling with container queries */
  @container/hero (min-width: 768px) {
    .hero-title {
      font-size: clamp(4rem, 8vw, 8rem);
    }
  }

  /* Performance optimizations */
  .animate-pulse,
  .glassmorphic-card,
  .animate-float-up {
    will-change: transform, opacity;
  }

  /* Smooth parallax for reduced motion preference */
  @media (prefers-reduced-motion: reduce) {
    .animate-float-up,
    .animate-fade-up {
      animation: none;
      opacity: 1;
      transform: none;
    }
    
    .glassmorphic-card:hover {
      transform: none;
    }
  }
</style>