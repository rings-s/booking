<!-- src/lib/components/subscription/PricingTable.svelte -->
<script>
    import { createEventDispatcher, onMount } from 'svelte';
    import PlanCard from './PlanCard.svelte';
    import Button from '../common/Button.svelte';
    import Spinner from '../common/Spinner.svelte';
    import { subscriptionAPI } from '$lib/api/subscriptions';
    import toast from 'svelte-french-toast';
    
    export let plans = [];
    export let currentPlanId = null;
    export let loading = false;
    export let billing = 'monthly'; // 'monthly', 'yearly'
    export let showComparison = false;
    
    const dispatch = createEventDispatcher();
    
    let selectedPlanId = null;
    let processingUpgrade = false;
    
    onMount(async () => {
      if (plans.length === 0) {
        await loadPlans();
      }
    });
    
    async function loadPlans() {
      loading = true;
      const { data, error } = await subscriptionAPI.getPlans();
      
      if (data) {
        plans = data;
      } else if (error) {
        toast.error(error);
      }
      
      loading = false;
    }
    
    function handleSelectPlan(event) {
      selectedPlanId = event.detail.id;
      dispatch('selectPlan', event.detail);
    }
    
    async function handleUpgrade() {
      if (!selectedPlanId) return;
      
      processingUpgrade = true;
      const { data, error } = await subscriptionAPI.createSubscription(selectedPlanId);
      
      if (data) {
        toast.success('Subscription upgraded successfully!');
        dispatch('upgraded', data);
      } else if (error) {
        toast.error(error);
      }
      
      processingUpgrade = false;
    }
    
    // Yearly pricing calculation (20% discount)
    $: displayPlans = Array.isArray(plans) ? plans.map(plan => ({
      ...plan,
      price: billing === 'yearly' ? plan.price * 12 * 0.8 : plan.price,
      originalPrice: billing === 'yearly' ? plan.price * 12 : null
    })) : [];
    
    // Feature comparison data
    const comparisonFeatures = [
      { key: 'max_services', label: 'Services', type: 'number' },
      { key: 'max_bookings_per_month', label: 'Monthly Bookings', type: 'number' },
      { key: 'max_staff_accounts', label: 'Staff Accounts', type: 'number' },
      { key: 'analytics_enabled', label: 'Analytics', type: 'boolean' },
      { key: 'priority_support', label: 'Priority Support', type: 'boolean' },
      { key: 'custom_branding', label: 'Custom Branding', type: 'boolean' },
      { key: 'api_access', label: 'API Access', type: 'boolean' },
      { key: 'email_reminders', label: 'Email Reminders', type: 'boolean' },
      { key: 'sms_reminders', label: 'SMS Reminders', type: 'boolean' },
      { key: 'online_payments', label: 'Online Payments', type: 'boolean' },
      { key: 'calendar_sync', label: 'Calendar Sync', type: 'boolean' },
      { key: 'data_export', label: 'Data Export', type: 'boolean' }
    ];
  </script>
  
  <div>
    <!-- Header -->
    <div class="text-center mb-12">
      <h2 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">
        Choose the perfect plan for your business
      </h2>
      <p class="mt-4 text-xl text-gray-600">
        Start with a free trial and upgrade anytime
      </p>
      
      <!-- Billing Toggle -->
      <div class="mt-6 flex justify-center">
        <div class="relative flex bg-gray-100 rounded-lg p-1">
          <button
            type="button"
            class="
              relative py-2 px-4 rounded-md text-sm font-medium transition-all
              {billing === 'monthly' 
                ? 'bg-white text-gray-900 shadow' 
                : 'text-gray-500 hover:text-gray-700'}
            "
            on:click={() => billing = 'monthly'}
          >
            Monthly
          </button>
          <button
            type="button"
            class="
              relative py-2 px-4 rounded-md text-sm font-medium transition-all
              {billing === 'yearly' 
                ? 'bg-white text-gray-900 shadow' 
                : 'text-gray-500 hover:text-gray-700'}
            "
            on:click={() => billing = 'yearly'}
          >
            Yearly
            <span class="ml-1 text-xs text-green-600">Save 20%</span>
          </button>
        </div>
      </div>
    </div>
    
    {#if loading}
      <div class="flex justify-center py-12">
        <Spinner size="lg">Loading plans...</Spinner>
      </div>
    {:else if !showComparison}
      <!-- Card View -->
      <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
        {#each displayPlans as plan, index}
          <div class="{index === 2 ? 'lg:scale-105' : ''}">
            <PlanCard
              {plan}
              currentPlan={plan.id === currentPlanId}
              recommended={plan.name === 'premium'}
              on:select={handleSelectPlan}
            />
          </div>
        {/each}
      </div>
    {:else}
      <!-- Comparison Table View -->
      <div class="mt-8 overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
        <table class="min-w-full divide-y divide-gray-300">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                Features
              </th>
              {#each displayPlans as plan}
                <th scope="col" class="px-3 py-3.5 text-center text-sm font-semibold text-gray-900">
                  <div>
                    <div class="text-lg capitalize">{plan.name}</div>
                    <div class="mt-1 text-2xl">
                      {#if plan.price === 0}
                        Free
                      {:else}
                        ${plan.price}/{billing === 'yearly' ? 'yr' : 'mo'}
                      {/if}
                    </div>
                    {#if plan.originalPrice}
                      <div class="text-xs text-gray-500 line-through">
                        ${plan.originalPrice}/yr
                      </div>
                    {/if}
                  </div>
                </th>
              {/each}
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 bg-white">
            {#each comparisonFeatures as feature}
              <tr>
                <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                  {feature.label}
                </td>
                {#each displayPlans as plan}
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500 text-center">
                    {#if feature.type === 'boolean'}
                      {#if plan[feature.key]}
                        <svg class="h-5 w-5 text-green-500 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                      {:else}
                        <svg class="h-5 w-5 text-gray-300 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      {/if}
                    {:else if feature.type === 'number'}
                      {plan[feature.key] === -1 ? 'Unlimited' : plan[feature.key]}
                    {:else}
                      {plan[feature.key]}
                    {/if}
                  </td>
                {/each}
              </tr>
            {/each}
            <tr>
              <td class="py-4 pl-4 pr-3 sm:pl-6"></td>
              {#each displayPlans as plan}
                <td class="px-3 py-4 text-center">
                  <Button
                    variant={plan.name === 'premium' ? 'primary' : 'outline'}
                    size="sm"
                    disabled={plan.id === currentPlanId}
                    on:click={() => handleSelectPlan({ detail: plan })}
                  >
                    {plan.id === currentPlanId ? 'Current' : 'Choose'}
                  </Button>
                </td>
              {/each}
            </tr>
          </tbody>
        </table>
      </div>
    {/if}
    
    <!-- Toggle View Button -->
    <div class="mt-8 text-center">
      <Button
        variant="outline"
        on:click={() => showComparison = !showComparison}
      >
        {showComparison ? 'View as Cards' : 'Compare Features'}
      </Button>
    </div>
    
    <!-- Trust Badges -->
    <div class="mt-12 border-t border-gray-200 pt-12">
      <div class="grid grid-cols-1 gap-8 sm:grid-cols-3">
        <div class="text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">Secure Payments</h3>
          <p class="mt-1 text-sm text-gray-500">SSL encrypted transactions</p>
        </div>
        
        <div class="text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">Cancel Anytime</h3>
          <p class="mt-1 text-sm text-gray-500">No long-term contracts</p>
        </div>
        
        <div class="text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">Instant Setup</h3>
          <p class="mt-1 text-sm text-gray-500">Start using immediately</p>
        </div>
      </div>
    </div>
  </div>