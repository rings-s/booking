<!-- src/routes/features/+page.svelte -->
<script>
  import { page } from '$app/stores';
  
  // Get feature from URL hash if available
  let activeFeature = null;
  $: if (typeof window !== 'undefined') {
    activeFeature = window.location.hash.slice(1);
  }
  
  const features = [
    {
      id: 'booking',
      title: 'Smart Booking System',
      description: 'Streamline your appointment scheduling with our intelligent booking system.',
      icon: 'calendar',
      details: [
        'Real-time availability checking',
        'Automated confirmations and reminders',
        'Calendar integration (Google, Outlook)',
        'Multiple service booking',
        'Recurring appointments'
      ]
    },
    {
      id: 'customers',
      title: 'Customer Management',
      description: 'Keep track of your customers and build lasting relationships.',
      icon: 'users',
      details: [
        'Customer profiles and history',
        'Automated follow-up communications',
        'Customer preferences tracking',
        'Loyalty program integration',
        'Review and feedback collection'
      ]
    },
    {
      id: 'payments',
      title: 'Secure Payments',
      description: 'Accept payments seamlessly with industry-leading security.',
      icon: 'credit-card',
      details: [
        'Stripe payment integration',
        'Multiple payment methods',
        'Automatic invoicing',
        'Payment tracking and reporting',
        'Refund management'
      ]
    },
    {
      id: 'analytics',
      title: 'Business Analytics',
      description: 'Make data-driven decisions with comprehensive analytics.',
      icon: 'chart',
      details: [
        'Revenue tracking and forecasting',
        'Customer behavior insights',
        'Service performance metrics',
        'Booking trends analysis',
        'Custom reporting dashboards'
      ]
    },
    {
      id: 'notifications',
      title: 'Smart Notifications',
      description: 'Keep everyone informed with automated communication.',
      icon: 'bell',
      details: [
        'SMS and email notifications',
        'Appointment reminders',
        'Booking confirmations',
        'Customizable message templates',
        'Multi-language support'
      ]
    },
    {
      id: 'mobile',
      title: 'Mobile Experience',
      description: 'Manage your business on-the-go with our mobile-optimized platform.',
      icon: 'mobile',
      details: [
        'Responsive mobile design',
        'Touch-friendly interface',
        'Offline booking capabilities',
        'Push notifications',
        'Mobile payment processing'
      ]
    }
  ];
  
  function getIconSvg(iconName) {
    const icons = {
      calendar: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />`,
      users: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />`,
      'credit-card': `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />`,
      chart: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />`,
      bell: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />`,
      mobile: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a1 1 0 001-1V4a1 1 0 00-1-1H8a1 1 0 00-1 1v16a1 1 0 001 1z" />`
    };
    return icons[iconName] || '';
  }
</script>

<svelte:head>
  <title>Features - BookingPro</title>
  <meta name="description" content="Discover all the powerful features BookingPro offers to streamline your business operations and enhance customer experience." />
</svelte:head>

<div class="bg-white">
  <!-- Hero Section -->
  <div class="relative bg-gradient-to-br from-indigo-600 to-purple-700">
    <div class="absolute inset-0 bg-black opacity-10"></div>
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="text-center">
        <h1 class="text-4xl md:text-6xl font-bold text-white mb-6">
          Powerful Features for
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-pink-400">
            Modern Businesses
          </span>
        </h1>
        <p class="text-xl text-indigo-100 max-w-3xl mx-auto mb-8">
          Everything you need to manage bookings, customers, and payments in one comprehensive platform.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a href="/auth/register" class="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-lg text-indigo-700 bg-white hover:bg-gray-50 transition-colors">
            Get Started Free
          </a>
          <a href="/businesses" class="inline-flex items-center px-8 py-3 border border-white text-base font-medium rounded-lg text-white hover:bg-white hover:text-indigo-700 transition-colors">
            View Businesses
          </a>
        </div>
      </div>
    </div>
  </div>

  <!-- Features Grid -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
    <div class="text-center mb-16">
      <h2 class="text-3xl font-bold text-gray-900 mb-4">Complete Business Solution</h2>
      <p class="text-lg text-gray-600 max-w-2xl mx-auto">
        Our comprehensive suite of tools helps you manage every aspect of your business efficiently.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {#each features as feature}
        <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 hover:shadow-xl transition-shadow duration-300" id={feature.id}>
          <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center mb-6">
            <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {@html getIconSvg(feature.icon)}
            </svg>
          </div>
          
          <h3 class="text-2xl font-bold text-gray-900 mb-4">{feature.title}</h3>
          <p class="text-gray-600 mb-6">{feature.description}</p>
          
          <ul class="space-y-3">
            {#each feature.details as detail}
              <li class="flex items-start">
                <svg class="w-5 h-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span class="text-gray-700 text-sm">{detail}</span>
              </li>
            {/each}
          </ul>
        </div>
      {/each}
    </div>
  </div>

  <!-- CTA Section -->
  <div class="bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="text-center">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">Ready to Get Started?</h2>
        <p class="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
          Join thousands of businesses already using BookingPro to streamline their operations and grow their customer base.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a href="/auth/register" class="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 transition-colors">
            Start Free Trial
          </a>
          <a href="/help" class="inline-flex items-center px-8 py-3 border border-gray-300 text-base font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 transition-colors">
            Learn More
          </a>
        </div>
      </div>
    </div>
  </div>
</div>