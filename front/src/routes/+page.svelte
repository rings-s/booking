<!-- src/routes/+page.svelte -->
<script>
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import Button from '$lib/components/common/Button.svelte';
  import { auth, isAuthenticated } from '$lib/stores/auth';
  import { businessAPI } from '$lib/api/businesses';
  import toast from 'svelte-french-toast';
  
  let emailInput = '';
  let subscribing = false;
  let featuredBusinesses = [];
  let loadingBusinesses = false;

  onMount(async () => {
    await loadFeaturedBusinesses();
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
</script>

<svelte:head>
  <title>BookingPro - Online Appointment Scheduling Made Simple</title>
  <meta name="description" content="Streamline your business with our powerful online booking system. Free trial, no setup fees, and 24/7 customer support.">
</svelte:head>

<div class="min-h-screen bg-white">
  <!-- Hero Section -->
  <section class="relative bg-gradient-to-br from-blue-50 to-indigo-100 py-20 lg:py-32">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center">
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
          Online Appointment
          <span class="text-blue-600">Scheduling</span>
          Made Simple
        </h1>
        <p class="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Streamline your business with our powerful booking system. Accept appointments 24/7, 
          reduce no-shows, and focus on what you do best.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <Button 
            size="lg" 
            class="px-8 py-4 text-lg font-semibold"
            on:click={handleGetStarted}
          >
            Start Free Trial
          </Button>
          <Button 
            variant="outline" 
            size="lg" 
            class="px-8 py-4 text-lg"
            on:click={() => goto('/demo')}
          >
            View Demo
          </Button>
        </div>
        <p class="text-sm text-gray-500 mt-4">
          Free 14-day trial • No credit card required • 50 appointments included
        </p>
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          Everything you need to manage bookings
        </h2>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Our comprehensive platform adapts to how you do business, not the other way around.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {#each features as feature}
          <div class="bg-white p-6 rounded-xl border border-gray-200 hover:shadow-lg transition-shadow duration-300">
            <div class="text-4xl mb-4">{feature.icon}</div>
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
      <div class="text-center mb-16">
        <h2 class="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          Perfect for every industry
        </h2>
        <p class="text-xl text-gray-600">
          Join thousands of businesses already using BookingPro
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {#each industries as industry}
          <div class="bg-white p-6 rounded-xl text-center border border-gray-200 hover:shadow-md transition-shadow duration-300">
            <div class="text-5xl mb-4">{industry.icon}</div>
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
      <div class="text-center mb-16">
        <h2 class="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          Loved by businesses worldwide
        </h2>
        <p class="text-xl text-gray-600">
          See what our customers have to say
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        {#each testimonials as testimonial}
          <div class="bg-gray-50 p-6 rounded-xl border border-gray-200">
            <div class="flex mb-4">
              {#each Array(testimonial.rating) as _}
                <span class="text-yellow-400 text-xl">★</span>
              {/each}
            </div>
            <blockquote class="text-gray-700 mb-4">
              "{testimonial.text}"
            </blockquote>
            <div class="flex items-center">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
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
      <div class="text-center mb-16">
        <h2 class="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
          Simple, transparent pricing
        </h2>
        <p class="text-xl text-gray-600">
          Start free, upgrade as you grow. No hidden fees, cancel anytime.
        </p>
      </div>

      <!-- Pricing Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Free Plan -->
        <div class="bg-white p-6 rounded-xl border-2 border-gray-200">
          <div class="text-center">
            <h3 class="text-xl font-bold text-gray-900 mb-2">Free</h3>
            <div class="text-3xl font-bold text-gray-900 mb-2">$0</div>
            <p class="text-gray-600 mb-6">Perfect for getting started</p>
          </div>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              50 bookings/month
            </li>
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              1 business
            </li>
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              5 services
            </li>
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Email notifications
            </li>
          </ul>
          <Button variant="outline" fullWidth on:click={handleGetStarted}>
            Get Started Free
          </Button>
        </div>

        <!-- Starter Plan -->
        <div class="bg-white p-6 rounded-xl border-2 border-gray-200">
          <div class="text-center">
            <h3 class="text-xl font-bold text-gray-900 mb-2">Starter</h3>
            <div class="text-3xl font-bold text-gray-900 mb-2">$9</div>
            <p class="text-gray-600 mb-6">For small businesses</p>
          </div>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              200 bookings/month
            </li>
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              2 businesses
            </li>
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              20 services total
            </li>
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Email reminders
            </li>
          </ul>
          <Button variant="outline" fullWidth on:click={handleGetStarted}>
            Start Free Trial
          </Button>
        </div>

        <!-- Professional Plan -->
        <div class="bg-blue-600 p-6 rounded-xl border-2 border-blue-600 relative">
          <div class="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <span class="bg-yellow-400 text-black px-3 py-1 rounded-full text-sm font-semibold">
              Most Popular
            </span>
          </div>
          <div class="text-center">
            <h3 class="text-xl font-bold text-white mb-2">Professional</h3>
            <div class="text-3xl font-bold text-white mb-2">$29</div>
            <p class="text-blue-100 mb-6">For growing businesses</p>
          </div>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center text-white">
              <svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              1,000 bookings/month
            </li>
            <li class="flex items-center text-white">
              <svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              5 businesses
            </li>
            <li class="flex items-center text-white">
              <svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Unlimited services
            </li>
            <li class="flex items-center text-white">
              <svg class="w-5 h-5 text-green-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Analytics dashboard
            </li>
          </ul>
          <Button variant="secondary" fullWidth on:click={handleGetStarted}>
            Start Free Trial
          </Button>
        </div>

        <!-- Business Plan -->
        <div class="bg-white p-6 rounded-xl border-2 border-gray-200">
          <div class="text-center">
            <h3 class="text-xl font-bold text-gray-900 mb-2">Business</h3>
            <div class="text-3xl font-bold text-gray-900 mb-2">$79</div>
            <p class="text-gray-600 mb-6">For large businesses</p>
          </div>
          <ul class="space-y-3 mb-8">
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              5,000 bookings/month
            </li>
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Unlimited businesses
            </li>
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Custom branding
            </li>
            <li class="flex items-center text-gray-700">
              <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
              </svg>
              Priority support
            </li>
          </ul>
          <Button variant="outline" fullWidth on:click={handleGetStarted}>
            Start Free Trial
          </Button>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA Section -->
  <section class="py-20 bg-blue-600 text-white">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h2 class="text-3xl lg:text-4xl font-bold mb-6">
        Ready to streamline your bookings?
      </h2>
      <p class="text-xl text-blue-100 mb-8">
        Join thousands of businesses already using BookingPro to save time and grow their business.
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <Button 
          variant="secondary" 
          size="lg" 
          class="px-8 py-4 text-lg font-semibold"
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
    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h3 class="text-2xl font-bold text-gray-900 mb-4">
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
          class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          required
        />
        <Button 
          type="submit" 
          disabled={subscribing}
          class="px-6 py-3 whitespace-nowrap"
        >
          {subscribing ? 'Subscribing...' : 'Subscribe'}
        </Button>
      </form>
    </div>
  </section>
</div>