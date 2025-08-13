<!-- src/lib/components/subscription/PlanCard.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
    import { formatCurrency } from '$lib/utils/formatters';
    import Button from '../common/Button.svelte';
    import { goto } from '$app/navigation';
    
    export let plan;
    export let currentPlan = false;
    export let recommended = false;
    export let loading = false;
    export let compact = false;
    
    const dispatch = createEventDispatcher();
    
    function handleSelect() {
      if (currentPlan) return;
      dispatch('select', plan);
    }
    
    function handleUpgrade() {
      goto(`/subscriptions/upgrade?plan=${plan.name}`);
    }
    
    // Feature list with icons
    const features = [
      {
        included: true,
        text: `Up to ${plan.max_services} services`,
        icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2'
      },
      {
        included: true,
        text: `${plan.max_bookings_per_month} bookings/month`,
        icon: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'
      },
      {
        included: true,
        text: `${plan.max_staff_accounts} staff account${plan.max_staff_accounts > 1 ? 's' : ''}`,
        icon: 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z'
      },
      {
        included: plan.analytics_enabled,
        text: 'Advanced analytics',
        icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
      },
      {
        included: plan.priority_support,
        text: 'Priority support',
        icon: 'M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z'
      },
      {
        included: plan.custom_branding,
        text: 'Custom branding',
        icon: 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01'
      },
      {
        included: plan.api_access,
        text: 'API access',
        icon: 'M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4'
      },
      {
        included: plan.email_reminders !== false,
        text: 'Email reminders',
        icon: 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z'
      }
    ];
    
    // Badge text based on plan type
    $: badgeText = plan.name === 'free' ? 'Free Forever' :
                   plan.name === 'basic' ? 'Most Popular' :
                   plan.name === 'premium' ? 'Best Value' :
                   plan.name === 'enterprise' ? 'Custom Solution' : '';
    
    $: planColor = plan.name === 'free' ? 'gray' :
                   plan.name === 'basic' ? 'blue' :
                   plan.name === 'premium' ? 'indigo' :
                   plan.name === 'enterprise' ? 'purple' : 'gray';
  </script>
  
  <div class="
    relative bg-white rounded-lg border-2 overflow-hidden transition-all duration-200
    {recommended ? 'border-indigo-600 shadow-xl scale-105' : 'border-gray-200 shadow-lg hover:shadow-xl'}
    {compact ? 'p-4' : 'p-6'}
  ">
    {#if recommended}
      <div class="absolute top-0 left-0 right-0 bg-indigo-600 text-white text-center py-1 text-sm font-medium">
        Recommended
      </div>
    {/if}
    
    {#if currentPlan}
      <div class="absolute top-0 right-0 bg-green-100 text-green-800 px-3 py-1 text-xs font-medium rounded-bl-lg">
        Current Plan
      </div>
    {/if}
    
    {#if badgeText && !currentPlan && !recommended}
      <div class="absolute top-0 right-0 bg-gray-100 text-gray-700 px-3 py-1 text-xs font-medium rounded-bl-lg">
        {badgeText}
      </div>
    {/if}
    
    <div class="{recommended ? 'mt-6' : ''}">
      <!-- Plan Name and Price -->
      <div class="text-center mb-6">
        <h3 class="text-2xl font-bold text-gray-900 capitalize">{plan.name}</h3>
        {#if plan.description}
          <p class="mt-2 text-sm text-gray-500">{plan.description}</p>
        {/if}
        
        <div class="mt-4">
          {#if plan.price === 0}
            <span class="text-4xl font-extrabold text-gray-900">Free</span>
          {:else}
            <span class="text-4xl font-extrabold text-gray-900">
              {formatCurrency(plan.price)}
            </span>
            <span class="text-base font-medium text-gray-500">/month</span>
          {/if}
        </div>
        
        {#if plan.trial_days && !currentPlan}
          <p class="mt-2 text-sm text-green-600">
            ✓ {plan.trial_days} day free trial
          </p>
        {/if}
      </div>
      
      <!-- Features List -->
      {#if !compact}
        <ul class="space-y-3 mb-6">
          {#each features.filter(f => f.included) as feature}
            <li class="flex items-start">
              <svg class="flex-shrink-0 h-5 w-5 text-green-500 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <div class="ml-3">
                <span class="text-sm text-gray-700">{feature.text}</span>
              </div>
            </li>
          {/each}
          
          {#each features.filter(f => !f.included).slice(0, 2) as feature}
            <li class="flex items-start opacity-40">
              <svg class="flex-shrink-0 h-5 w-5 text-gray-400 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <div class="ml-3">
                <span class="text-sm text-gray-500 line-through">{feature.text}</span>
              </div>
            </li>
          {/each}
        </ul>
      {/if}
      
      <!-- Action Button -->
      <div>
        {#if currentPlan}
          <Button fullWidth disabled variant="outline">
            <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            Current Plan
          </Button>
        {:else}
          <Button
            fullWidth
            variant={recommended ? 'primary' : 'outline'}
            on:click={handleSelect}
            {loading}
          >
            {#if plan.price === 0}
              Get Started Free
            {:else if plan.trial_days}
              Start {plan.trial_days}-Day Trial
            {:else}
              Choose {plan.name}
            {/if}
          </Button>
        {/if}
      </div>
      
      {#if plan.name === 'enterprise'}
        <p class="mt-3 text-center text-xs text-gray-500">
          Contact us for custom pricing
        </p>
      {/if}
    </div>
  </div>