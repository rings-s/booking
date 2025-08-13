<!-- src/routes/subscriptions/upgrade/+page.svelte -->
<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { subscriptionAPI } from '$lib/api/subscriptions';
    import { auth } from '$lib/stores/auth';
    import PlanCard from '$lib/components/subscription/PlanCard.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Alert from '$lib/components/common/Alert.svelte';
    import Input from '$lib/components/common/Input.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import toast from 'svelte-french-toast';
    import { loadStripe } from '@stripe/stripe-js';
    
    let loading = true;
    let processing = false;
    let currentSubscription = null;
    let selectedPlan = null;
    let plans = [];
    let billingCycle = 'monthly';
    let showPaymentModal = false;
    let showConfirmModal = false;
    let promoCode = '';
    let applyingPromo = false;
    let discount = null;
    
    // Payment form
    let paymentData = {
      card_number: '',
      card_name: '',
      exp_month: '',
      exp_year: '',
      cvc: '',
      billing_address: '',
      billing_city: '',
      billing_state: '',
      billing_zip: '',
      billing_country: 'US'
    };
    
    // Stripe elements
    let stripe = null;
    let elements = null;
    let cardElement = null;
    
    const planId = $page.url.searchParams.get('plan');
    
    onMount(async () => {
      await loadPlans();
      await loadCurrentSubscription();
      await initializeStripe();
      
      // Pre-select plan if provided in URL
      if (planId) {
        selectedPlan = plans.find(p => p.id === planId);
      }
    });
    
    async function loadPlans() {
      const { data, error } = await subscriptionAPI.getPlans();
      
      if (data) {
        plans = data;
      } else {
        toast.error('Failed to load plans');
        goto('/subscriptions');
      }
    }
    
    async function loadCurrentSubscription() {
      const { data } = await subscriptionAPI.getCurrentSubscription();
      
      if (data) {
        currentSubscription = data;
      }
      
      loading = false;
    }
    
    async function initializeStripe() {
      const { data } = await subscriptionAPI.getStripePublicKey();
      
      if (data?.public_key) {
        stripe = await loadStripe(data.public_key);
        elements = stripe.elements();
        
        // Create card element
        cardElement = elements.create('card', {
          style: {
            base: {
              fontSize: '16px',
              color: '#424770',
              '::placeholder': {
                color: '#aab7c4',
              },
            },
            invalid: {
              color: '#9e2146',
            },
          },
        });
      }
    }
    
    function selectPlan(plan) {
      if (currentSubscription && plan.id === currentSubscription.plan.id) {
        toast.error('You are already on this plan');
        return;
      }
      
      selectedPlan = plan;
    }
    
    async function applyPromoCode() {
      if (!promoCode) {
        toast.error('Please enter a promo code');
        return;
      }
      
      applyingPromo = true;
      
      const { data, error } = await subscriptionAPI.validatePromoCode(promoCode);
      
      if (data) {
        discount = data;
        toast.success(`Promo code applied: ${data.description}`);
      } else {
        toast.error(error || 'Invalid promo code');
      }
      
      applyingPromo = false;
    }
    
    function removePromoCode() {
      discount = null;
      promoCode = '';
    }
    
    async function handleContinue() {
      if (!selectedPlan) {
        toast.error('Please select a plan');
        return;
      }
      
      if (currentSubscription) {
        // Show confirmation for plan change
        showConfirmModal = true;
      } else {
        // New subscription - show payment form
        showPaymentModal = true;
        
        // Mount Stripe card element
        if (cardElement && !cardElement._mounted) {
          setTimeout(() => {
            const cardDiv = document.getElementById('card-element');
            if (cardDiv) {
              cardElement.mount(cardDiv);
            }
          }, 100);
        }
      }
    }
    
    async function confirmPlanChange() {
      processing = true;
      
      const payload = {
        plan_id: selectedPlan.id,
        billing_cycle: billingCycle,
        promo_code: discount ? promoCode : null
      };
      
      const { data, error } = await subscriptionAPI.changePlan(
        currentSubscription.id,
        payload
      );
      
      if (data) {
        toast.success('Plan changed successfully!');
        goto('/subscriptions');
      } else {
        toast.error(error || 'Failed to change plan');
      }
      
      processing = false;
    }
    
    async function processPayment() {
      if (!stripe || !cardElement) {
        toast.error('Payment system not initialized');
        return;
      }
      
      processing = true;
      
      // Create payment method with Stripe
      const { error: stripeError, paymentMethod } = await stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
        billing_details: {
          name: paymentData.card_name,
          address: {
            line1: paymentData.billing_address,
            city: paymentData.billing_city,
            state: paymentData.billing_state,
            postal_code: paymentData.billing_zip,
            country: paymentData.billing_country
          }
        }
      });
      
      if (stripeError) {
        toast.error(stripeError.message);
        processing = false;
        return;
      }
      
      // Create subscription
      const payload = {
        plan_id: selectedPlan.id,
        billing_cycle: billingCycle,
        payment_method_id: paymentMethod.id,
        promo_code: discount ? promoCode : null,
        billing_details: {
          address: paymentData.billing_address,
          city: paymentData.billing_city,
          state: paymentData.billing_state,
          zip: paymentData.billing_zip,
          country: paymentData.billing_country
        }
      };
      
      const { data, error } = await subscriptionAPI.createSubscription(payload);
      
      if (data) {
        if (data.status === 'requires_action') {
          // Handle 3D Secure authentication
          const { error: confirmError } = await stripe.confirmCardPayment(
            data.client_secret
          );
          
          if (confirmError) {
            toast.error('Payment authentication failed');
          } else {
            toast.success('Subscription created successfully!');
            goto('/subscriptions');
          }
        } else {
          toast.success('Subscription created successfully!');
          goto('/subscriptions');
        }
      } else {
        toast.error(error || 'Failed to create subscription');
      }
      
      processing = false;
    }
    
    // Calculate pricing
    $: monthlyPrice = selectedPlan ? selectedPlan.price : 0;
    $: yearlyPrice = selectedPlan ? selectedPlan.price * 12 * 0.8 : 0; // 20% discount
    $: displayPrice = billingCycle === 'yearly' ? yearlyPrice : monthlyPrice;
    $: discountAmount = discount ? (displayPrice * discount.percent_off / 100) : 0;
    $: finalPrice = displayPrice - discountAmount;
    $: savings = billingCycle === 'yearly' ? (selectedPlan?.price * 12 - yearlyPrice) : 0;
    
    // Check if downgrading
    $: isDowngrade = currentSubscription && selectedPlan && 
      selectedPlan.price < currentSubscription.plan.price;
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-3xl font-bold text-gray-900">
          {currentSubscription ? 'Change Your Plan' : 'Choose Your Plan'}
        </h1>
        <p class="mt-2 text-gray-600">
          {currentSubscription 
            ? 'Select a new plan that better fits your needs'
            : 'Start your free trial today and upgrade anytime'}
        </p>
      </div>
      
      {#if loading}
        <div class="flex justify-center py-12">
          <Spinner size="lg">Loading plans...</Spinner>
        </div>
      {:else}
        <!-- Current Plan Alert -->
        {#if currentSubscription}
          <Alert type="info" class="mb-8">
            <div class="flex items-center justify-between">
              <div>
                <p class="font-medium">Current Plan: {currentSubscription.plan.name}</p>
                <p class="text-sm mt-1">
                  ${currentSubscription.plan.price}/month • 
                  Next billing date: {new Date(currentSubscription.current_period_end).toLocaleDateString()}
                </p>
              </div>
              <span class="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium">
                Active
              </span>
            </div>
          </Alert>
        {/if}
        
        <!-- Billing Cycle Toggle -->
        <div class="flex justify-center mb-8">
          <div class="bg-white rounded-lg shadow-sm p-1 flex">
            <button
              class="px-6 py-2 rounded-md text-sm font-medium transition-all
                     {billingCycle === 'monthly' 
                       ? 'bg-indigo-600 text-white' 
                       : 'text-gray-700 hover:text-gray-900'}"
              on:click={() => billingCycle = 'monthly'}
            >
              Monthly
            </button>
            <button
              class="px-6 py-2 rounded-md text-sm font-medium transition-all
                     {billingCycle === 'yearly' 
                       ? 'bg-indigo-600 text-white' 
                       : 'text-gray-700 hover:text-gray-900'}"
              on:click={() => billingCycle = 'yearly'}
            >
              Yearly
              <span class="ml-1 text-xs {billingCycle === 'yearly' ? 'text-indigo-200' : 'text-green-600'}">
                Save 20%
              </span>
            </button>
          </div>
        </div>
        
        <!-- Plans Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {#each plans as plan}
            {@const isCurrentPlan = currentSubscription?.plan.id === plan.id}
            {@const price = billingCycle === 'yearly' ? plan.price * 12 * 0.8 : plan.price}
            
            <div class="relative">
              {#if plan.recommended}
                <div class="absolute -top-3 left-1/2 transform -translate-x-1/2 z-10">
                  <span class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-3 py-1 rounded-full text-xs font-semibold">
                    RECOMMENDED
                  </span>
                </div>
              {/if}
              
              <Card class="h-full {selectedPlan?.id === plan.id ? 'ring-2 ring-indigo-600' : ''}">
                <div class="p-6">
                  <!-- Plan Name -->
                  <h3 class="text-xl font-bold text-gray-900 text-center">
                    {plan.name}
                  </h3>
                  
                  <!-- Price -->
                  <div class="mt-4 text-center">
                    {#if plan.price === 0}
                      <span class="text-4xl font-extrabold text-gray-900">Free</span>
                    {:else}
                      <span class="text-4xl font-extrabold text-gray-900">
                        ${billingCycle === 'yearly' ? Math.round(price / 12) : price}
                      </span>
                      <span class="text-gray-500">/month</span>
                      {#if billingCycle === 'yearly'}
                        <p class="text-sm text-gray-500 mt-1">
                          Billed ${price} yearly
                        </p>
                      {/if}
                    {/if}
                  </div>
                  
                  <!-- Features -->
                  <ul class="mt-6 space-y-3">
                    <li class="flex items-start">
                      <svg class="w-5 h-5 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                      <span class="ml-2 text-sm text-gray-700">
                        {plan.max_bookings_per_month === -1 ? 'Unlimited' : plan.max_bookings_per_month} bookings/month
                      </span>
                    </li>
                    
                    <li class="flex items-start">
                      <svg class="w-5 h-5 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                      <span class="ml-2 text-sm text-gray-700">
                        Up to {plan.max_services} services
                      </span>
                    </li>
                    
                    <li class="flex items-start">
                      <svg class="w-5 h-5 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                      <span class="ml-2 text-sm text-gray-700">
                        {plan.max_staff_accounts} staff accounts
                      </span>
                    </li>
                    
                    {#if plan.analytics_enabled}
                      <li class="flex items-start">
                        <svg class="w-5 h-5 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                        <span class="ml-2 text-sm text-gray-700">Advanced analytics</span>
                      </li>
                    {/if}
                    
                    {#if plan.priority_support}
                      <li class="flex items-start">
                        <svg class="w-5 h-5 text-green-500 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                        <span class="ml-2 text-sm text-gray-700">Priority support</span>
                      </li>
                    {/if}
                  </ul>
                  
                  <!-- Select Button -->
                  <div class="mt-6">
                    {#if isCurrentPlan}
                      <Button fullWidth disabled variant="outline">
                        Current Plan
                      </Button>
                    {:else}
                      <Button
                        fullWidth
                        variant={selectedPlan?.id === plan.id ? 'primary' : 'outline'}
                        on:click={() => selectPlan(plan)}
                      >
                        {selectedPlan?.id === plan.id ? 'Selected' : 'Select Plan'}
                      </Button>
                    {/if}
                  </div>
                </div>
              </Card>
            </div>
          {/each}
        </div>
        
        <!-- Promo Code Section -->
        <Card class="mb-8">
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Have a promo code?</h3>
            
            {#if discount}
              <div class="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                <div>
                  <p class="font-medium text-green-900">{discount.description}</p>
                  <p class="text-sm text-green-700">
                    {discount.percent_off}% off 
                    {discount.duration === 'forever' ? 'forever' : `for ${discount.duration_in_months} months`}
                  </p>
                </div>
                <Button size="sm" variant="outline" on:click={removePromoCode}>
                  Remove
                </Button>
              </div>
            {:else}
              <div class="flex gap-3">
                <Input
                  bind:value={promoCode}
                  placeholder="Enter promo code"
                  class="flex-1"
                />
                <Button
                  on:click={applyPromoCode}
                  loading={applyingPromo}
                >
                  Apply
                </Button>
              </div>
            {/if}
          </div>
        </Card>
        
        <!-- Order Summary -->
        {#if selectedPlan}
          <Card class="mb-8">
            <div class="p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Order Summary</h3>
              
              <dl class="space-y-3">
                <div class="flex justify-between">
                  <dt class="text-gray-600">Plan</dt>
                  <dd class="font-medium text-gray-900">{selectedPlan.name}</dd>
                </div>
                
                <div class="flex justify-between">
                  <dt class="text-gray-600">Billing Cycle</dt>
                  <dd class="font-medium text-gray-900">
                    {billingCycle === 'yearly' ? 'Yearly' : 'Monthly'}
                  </dd>
                </div>
                
                <div class="flex justify-between">
                  <dt class="text-gray-600">Base Price</dt>
                  <dd class="font-medium text-gray-900">
                    ${displayPrice}{billingCycle === 'yearly' ? '/year' : '/month'}
                  </dd>
                </div>
                
                {#if discount}
                  <div class="flex justify-between text-green-600">
                    <dt>Discount ({discount.percent_off}%)</dt>
                    <dd class="font-medium">-${discountAmount.toFixed(2)}</dd>
                  </div>
                {/if}
                
                {#if billingCycle === 'yearly'}
                  <div class="flex justify-between text-green-600">
                    <dt>Annual Savings</dt>
                    <dd class="font-medium">${savings.toFixed(2)}</dd>
                  </div>
                {/if}
                
                <div class="pt-3 border-t border-gray-200">
                  <div class="flex justify-between">
                    <dt class="text-lg font-semibold text-gray-900">Total</dt>
                    <dd class="text-lg font-bold text-gray-900">
                      ${finalPrice.toFixed(2)}{billingCycle === 'yearly' ? '/year' : '/month'}
                    </dd>
                  </div>
                </div>
              </dl>
              
              {#if isDowngrade}
                <Alert type="warning" class="mt-4">
                  You are downgrading your plan. Some features may become unavailable.
                </Alert>
              {/if}
              
              <div class="mt-6">
                <Button fullWidth size="lg" on:click={handleContinue}>
                  {currentSubscription ? 'Continue to Confirmation' : 'Continue to Payment'}
                </Button>
              </div>
            </div>
          </Card>
        {/if}
        
        <!-- Features Comparison -->
        <Card>
          <div class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">All Features Comparison</h3>
            
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Feature
                    </th>
                    {#each plans as plan}
                      <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                        {plan.name}
                      </th>
                    {/each}
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  <tr>
                    <td class="px-6 py-4 text-sm text-gray-900">Monthly Bookings</td>
                    {#each plans as plan}
                      <td class="px-6 py-4 text-sm text-center text-gray-600">
                        {plan.max_bookings_per_month === -1 ? 'Unlimited' : plan.max_bookings_per_month}
                      </td>
                    {/each}
                  </tr>
                  
                  <tr>
                    <td class="px-6 py-4 text-sm text-gray-900">Services</td>
                    {#each plans as plan}
                      <td class="px-6 py-4 text-sm text-center text-gray-600">
                        {plan.max_services === -1 ? 'Unlimited' : plan.max_services}
                      </td>
                    {/each}
                  </tr>
                  
                  <tr>
                    <td class="px-6 py-4 text-sm text-gray-900">Staff Accounts</td>
                    {#each plans as plan}
                      <td class="px-6 py-4 text-sm text-center text-gray-600">
                        {plan.max_staff_accounts}
                      </td>
                    {/each}
                  </tr>
                  
                  <tr>
                    <td class="px-6 py-4 text-sm text-gray-900">Analytics</td>
                    {#each plans as plan}
                      <td class="px-6 py-4 text-sm text-center">
                        {#if plan.analytics_enabled}
                          <svg class="w-5 h-5 text-green-500 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                          </svg>
                        {:else}
                          <svg class="w-5 h-5 text-gray-300 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        {/if}
                      </td>
                    {/each}
                  </tr>
                  
                  <tr>
                    <td class="px-6 py-4 text-sm text-gray-900">Priority Support</td>
                    {#each plans as plan}
                      <td class="px-6 py-4 text-sm text-center">
                        {#if plan.priority_support}
                          <svg class="w-5 h-5 text-green-500 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                          </svg>
                        {:else}
                          <svg class="w-5 h-5 text-gray-300 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                        {/if}
                      </td>
                    {/each}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </Card>
      {/if}
    </div>
    
    <!-- Payment Modal -->
    <Modal bind:open={showPaymentModal} title="Payment Information" size="lg">
      <div class="space-y-6">
        <!-- Payment Method -->
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-4">Payment Method</h3>
          
          <div class="space-y-4">
            <Input
              label="Cardholder Name"
              bind:value={paymentData.card_name}
              required
              placeholder="John Doe"
            />
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Card Details
              </label>
              <div id="card-element" class="p-3 border border-gray-300 rounded-lg"></div>
            </div>
          </div>
        </div>
        
        <!-- Billing Address -->
        <div>
          <h3 class="text-lg font-medium text-gray-900 mb-4">Billing Address</h3>
          
          <div class="space-y-4">
            <Input
              label="Street Address"
              bind:value={paymentData.billing_address}
              required
              placeholder="123 Main St"
            />
            
            <div class="grid grid-cols-2 gap-4">
              <Input
                label="City"
                bind:value={paymentData.billing_city}
                required
                placeholder="New York"
              />
              
              <Input
                label="State"
                bind:value={paymentData.billing_state}
                required
                placeholder="NY"
              />
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <Input
                label="ZIP Code"
                bind:value={paymentData.billing_zip}
                required
                placeholder="10001"
              />
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Country
                </label>
                <select
                  bind:value={paymentData.billing_country}
                  class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                >
                  <option value="US">United States</option>
                  <option value="CA">Canada</option>
                  <option value="GB">United Kingdom</option>
                  <option value="AU">Australia</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Terms -->
        <div class="bg-gray-50 rounded-lg p-4">
          <p class="text-sm text-gray-600">
            By subscribing, you agree to our Terms of Service and authorize us to charge your payment method on a recurring basis.
            You can cancel anytime from your account settings.
          </p>
        </div>
      </div>
      
      <div slot="footer" class="flex justify-between">
        <Button variant="outline" on:click={() => showPaymentModal = false}>
          Back
        </Button>
        
        <Button on:click={processPayment} loading={processing}>
          Subscribe (${finalPrice.toFixed(2)}/{billingCycle === 'yearly' ? 'year' : 'month'})
        </Button>
      </div>
    </Modal>
    
    <!-- Confirmation Modal (for existing subscriptions) -->
    <Modal bind:open={showConfirmModal} title="Confirm Plan Change" size="md">
      <div class="space-y-4">
        {#if isDowngrade}
          <Alert type="warning">
            <strong>Important:</strong> You are downgrading your plan. Some features may become unavailable immediately.
          </Alert>
        {/if}
        
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="font-medium text-gray-900 mb-3">Plan Change Summary</h4>
          
          <dl class="space-y-2 text-sm">
            <div class="flex justify-between">
              <dt class="text-gray-600">Current Plan:</dt>
              <dd class="font-medium text-gray-900">{currentSubscription?.plan.name}</dd>
            </div>
            
            <div class="flex justify-between">
              <dt class="text-gray-600">New Plan:</dt>
              <dd class="font-medium text-gray-900">{selectedPlan?.name}</dd>
            </div>
            
            <div class="flex justify-between">
              <dt class="text-gray-600">Price Change:</dt>
              <dd class="font-medium {isDowngrade ? 'text-green-600' : 'text-red-600'}">
                {isDowngrade ? '-' : '+'}${Math.abs((selectedPlan?.price || 0) - (currentSubscription?.plan.price || 0))}/month
              </dd>
            </div>
          </dl>
        </div>
        
        <p class="text-sm text-gray-600">
          Your new plan will take effect immediately. 
          {isDowngrade 
            ? 'You will receive a prorated credit for the unused time on your current plan.'
            : 'You will be charged a prorated amount for the remainder of your billing period.'}
        </p>
      </div>
      
      <div slot="footer" class="flex justify-between">
        <Button variant="outline" on:click={() => showConfirmModal = false}>
          Cancel
        </Button>
        
        <Button on:click={confirmPlanChange} loading={processing}>
          Confirm Change
        </Button>
      </div>
    </Modal>
  </div>