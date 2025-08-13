<!-- src/routes/help/+page.svelte -->
<script>
  import { onMount } from 'svelte';
  import Input from '$lib/components/common/Input.svelte';
  import Button from '$lib/components/common/Button.svelte';
  
  let searchQuery = '';
  let activeCategory = 'all';
  
  const categories = [
    { id: 'all', name: 'All Topics', icon: 'collection' },
    { id: 'getting-started', name: 'Getting Started', icon: 'play' },
    { id: 'booking', name: 'Booking & Scheduling', icon: 'calendar' },
    { id: 'payments', name: 'Payments & Billing', icon: 'credit-card' },
    { id: 'customers', name: 'Customer Management', icon: 'users' },
    { id: 'account', name: 'Account Settings', icon: 'cog' }
  ];
  
  const helpArticles = [
    {
      id: 1,
      title: 'How to Create Your First Business Profile',
      category: 'getting-started',
      content: 'Learn how to set up your business profile with all the essential information.',
      popular: true
    },
    {
      id: 2,
      title: 'Setting Up Your Services and Pricing',
      category: 'getting-started',
      content: 'Configure your services, pricing, and availability for customer bookings.'
    },
    {
      id: 3,
      title: 'Managing Customer Bookings',
      category: 'booking',
      content: 'Accept, modify, and cancel customer bookings efficiently.',
      popular: true
    },
    {
      id: 4,
      title: 'Configuring Payment Methods',
      category: 'payments',
      content: 'Set up Stripe integration and configure payment processing.'
    },
    {
      id: 5,
      title: 'Understanding Your Dashboard Analytics',
      category: 'booking',
      content: 'Interpret your business metrics and performance data.'
    },
    {
      id: 6,
      title: 'Managing Customer Information',
      category: 'customers',
      content: 'Add, edit, and organize your customer database.'
    },
    {
      id: 7,
      title: 'Customizing Notification Settings',
      category: 'account',
      content: 'Configure email and SMS notifications for your business.'
    },
    {
      id: 8,
      title: 'Handling Refunds and Cancellations',
      category: 'payments',
      content: 'Process refunds and manage cancellation policies.'
    }
  ];
  
  const faqs = [
    {
      question: 'How do I reset my password?',
      answer: 'Go to the login page and click "Forgot password". Enter your email address and follow the instructions sent to your inbox.'
    },
    {
      question: 'Can customers book multiple services at once?',
      answer: 'Yes, customers can select multiple services during the booking process. The system will automatically calculate total time and cost.'
    },
    {
      question: 'What payment methods do you support?',
      answer: 'We support all major credit cards, debit cards, and digital wallets through our Stripe integration.'
    },
    {
      question: 'How do I change my business hours?',
      answer: 'Navigate to your business settings and update the "Business Hours" section. Changes will be reflected immediately on your booking page.'
    },
    {
      question: 'Is there a mobile app available?',
      answer: 'Currently, we offer a mobile-optimized web experience. A dedicated mobile app is in development.'
    }
  ];
  
  $: filteredArticles = helpArticles.filter(article => {
    const matchesSearch = article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         article.content.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = activeCategory === 'all' || article.category === activeCategory;
    return matchesSearch && matchesCategory;
  });
  
  function getIconSvg(iconName) {
    const icons = {
      collection: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />`,
      play: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h8m-1 0a9 9 0 11-8 0h8z" />`,
      calendar: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />`,
      'credit-card': `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />`,
      users: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />`,
      cog: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />`
    };
    return icons[iconName] || '';
  }
  
  let openFaq = null;
  
  function toggleFaq(index) {
    openFaq = openFaq === index ? null : index;
  }
</script>

<svelte:head>
  <title>Help Center - BookingPro</title>
  <meta name="description" content="Find answers to common questions and learn how to get the most out of BookingPro." />
</svelte:head>

<div class="bg-white">
  <!-- Hero Section -->
  <div class="bg-gradient-to-br from-indigo-600 to-purple-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="text-center">
        <h1 class="text-4xl md:text-5xl font-bold text-white mb-6">
          How can we help you?
        </h1>
        <p class="text-xl text-indigo-100 mb-8 max-w-2xl mx-auto">
          Search our knowledge base or browse categories to find answers to your questions.
        </p>
        
        <!-- Search Bar -->
        <div class="max-w-2xl mx-auto">
          <div class="relative">
            <Input
              bind:value={searchQuery}
              placeholder="Search for help articles..."
              class="!bg-white !text-gray-900 !pr-12"
            />
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
              <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <!-- Categories Sidebar -->
      <div class="lg:col-span-1">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Categories</h3>
        <nav class="space-y-1">
          {#each categories as category}
            <button
              on:click={() => activeCategory = category.id}
              class="
                w-full flex items-center px-3 py-2 text-sm font-medium rounded-lg text-left transition-colors
                {activeCategory === category.id
                  ? 'bg-indigo-100 text-indigo-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}
              "
            >
              <svg class="w-5 h-5 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {@html getIconSvg(category.icon)}
              </svg>
              {category.name}
            </button>
          {/each}
        </nav>
        
        <!-- Contact Support -->
        <div class="mt-8 bg-gray-50 rounded-lg p-4">
          <h4 class="text-sm font-medium text-gray-900 mb-2">Still need help?</h4>
          <p class="text-sm text-gray-600 mb-3">
            Can't find what you're looking for? Contact our support team.
          </p>
          <Button size="sm" variant="outline" fullWidth>
            Contact Support
          </Button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="lg:col-span-3">
        <!-- Popular Articles -->
        {#if activeCategory === 'all' && !searchQuery}
          <div class="mb-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Popular Articles</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              {#each helpArticles.filter(article => article.popular) as article}
                <div class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                  <h3 class="text-lg font-semibold text-gray-900 mb-2">{article.title}</h3>
                  <p class="text-gray-600 mb-4">{article.content}</p>
                  <div class="flex items-center justify-between">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                      {categories.find(cat => cat.id === article.category)?.name}
                    </span>
                    <button class="text-indigo-600 hover:text-indigo-500 text-sm font-medium">
                      Read more →
                    </button>
                  </div>
                </div>
              {/each}
            </div>
          </div>
        {/if}

        <!-- All Articles -->
        <div class="mb-12">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">
            {searchQuery ? `Search Results (${filteredArticles.length})` : 'All Articles'}
          </h2>
          
          {#if filteredArticles.length === 0}
            <div class="text-center py-12">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <h3 class="mt-2 text-sm font-medium text-gray-900">No articles found</h3>
              <p class="mt-1 text-sm text-gray-500">Try adjusting your search or browse categories.</p>
            </div>
          {:else}
            <div class="space-y-4">
              {#each filteredArticles as article}
                <div class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                  <div class="flex items-start justify-between">
                    <div class="flex-1">
                      <h3 class="text-lg font-semibold text-gray-900 mb-2">{article.title}</h3>
                      <p class="text-gray-600 mb-3">{article.content}</p>
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                        {categories.find(cat => cat.id === article.category)?.name}
                      </span>
                    </div>
                    <button class="ml-4 text-indigo-600 hover:text-indigo-500 text-sm font-medium whitespace-nowrap">
                      Read more →
                    </button>
                  </div>
                </div>
              {/each}
            </div>
          {/if}
        </div>

        <!-- FAQ Section -->
        <div>
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Frequently Asked Questions</h2>
          <div class="space-y-4">
            {#each faqs as faq, index}
              <div class="bg-white border border-gray-200 rounded-lg">
                <button
                  on:click={() => toggleFaq(index)}
                  class="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50"
                >
                  <span class="font-medium text-gray-900">{faq.question}</span>
                  <svg 
                    class="w-5 h-5 text-gray-500 transition-transform {openFaq === index ? 'rotate-180' : ''}"
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                
                {#if openFaq === index}
                  <div class="px-6 pb-4">
                    <p class="text-gray-600">{faq.answer}</p>
                  </div>
                {/if}
              </div>
            {/each}
          </div>
        </div>
      </div>
    </div>
  </div>
</div>