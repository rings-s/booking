<!-- src/routes/subscriptions/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { subscriptionAPI } from '$lib/api/subscriptions';
    import { auth } from '$lib/stores/auth';
    import PricingTable from '$lib/components/subscription/PricingTable.svelte';
    import SubscriptionStatus from '$lib/components/subscription/SubscriptionStatus.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Alert from '$lib/components/common/Alert.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import toast from 'svelte-french-toast';
    
    let loading = true;
    let currentSubscription = null;
    let plans = [];
    let invoices = [];
    let usage = null;
    let activeTab = 'overview';
    
    onMount(async () => {
      await loadSubscriptionData();
    });
    
    async function loadSubscriptionData() {
      loading = true;
      
      const [subRes, plansRes, invoicesRes, usageRes] = await Promise.all([
        subscriptionAPI.getCurrentSubscription(),
        subscriptionAPI.getPlans(),
        subscriptionAPI.getInvoices(),
        subscriptionAPI.getUsage()
      ]);
      
      if (subRes.data) currentSubscription = subRes.data;
      if (plansRes.data) plans = plansRes.data;
      if (invoicesRes.data) invoices = invoicesRes.data;
      if (usageRes.data) usage = usageRes.data;
      
      loading = false;
    }
    
    async function handlePlanSelect(event) {
      const plan = event.detail;
      
      if (currentSubscription && plan.id === currentSubscription.plan.id) {
        toast.error('You are already on this plan');
        return;
      }
      
      goto(`/subscriptions/upgrade?plan=${plan.id}`);
    }
    
    async function downloadInvoice(invoiceId) {
      const { data, error } = await subscriptionAPI.downloadInvoice(invoiceId);
      
      if (data) {
        const blob = new Blob([data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `invoice-${invoiceId}.pdf`;
        link.click();
        
        toast.success('Invoice downloaded');
      } else {
        toast.error('Failed to download invoice');
      }
    }
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6">
          <h1 class="text-2xl font-bold text-gray-900">Subscription & Billing</h1>
          <p class="mt-1 text-sm text-gray-600">
            Manage your subscription plan and billing information
          </p>
        </div>
      </div>
    </div>
    
    <!-- Tabs -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex space-x-8">
          {#each ['overview', 'plans', 'invoices'] as tab}
            <button
              class="py-4 px-1 border-b-2 font-medium text-sm transition-colors
                     {activeTab === tab 
                       ? 'border-indigo-500 text-indigo-600' 
                       : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
              on:click={() => activeTab = tab}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          {/each}
        </div>
      </div>
    </div>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {#if loading}
        <div class="flex justify-center py-12">
          <Spinner size="lg">Loading subscription data...</Spinner>
        </div>
      {:else if activeTab === 'overview'}
        <!-- Overview Tab -->
        <div class="space-y-6">
          <SubscriptionStatus
            subscription={currentSubscription}
            {usage}
          />
          
          {#if currentSubscription}
            <!-- Payment Method -->
            <Card title="Payment Method">
              <div class="flex items-center justify-between">
                {#if currentSubscription.payment_method}
                  <div class="flex items-center space-x-4">
                    <div class="p-3 bg-gray-100 rounded-lg">
                      <svg class="w-8 h-5" viewBox="0 0 32 20">
                        <!-- Card icon -->
                        <rect width="32" height="20" rx="4" fill="#1f2937"/>
                        <rect x="2" y="8" width="28" height="4" fill="#4b5563"/>
                      </svg>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900">
                        •••• •••• •••• {currentSubscription.payment_method.last4}
                      </p>
                      <p class="text-xs text-gray-500">
                        Expires {currentSubscription.payment_method.exp_month}/{currentSubscription.payment_method.exp_year}
                      </p>
                    </div>
                  </div>
                  
                  <Button variant="outline" size="sm">
                    Update
                  </Button>
                {:else}
                  <div>
                    <p class="text-sm text-gray-600">No payment method on file</p>
                  </div>
                  
                  <Button size="sm">
                    Add Payment Method
                  </Button>
                {/if}
              </div>
            </Card>
            
            <!-- Billing Address -->
            <Card title="Billing Information">
              <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <dt class="text-sm font-medium text-gray-500">Billing Email</dt>
                  <dd class="mt-1 text-sm text-gray-900">
                    {currentSubscription.billing_email || $auth.user?.email}
                  </dd>
                </div>
                
                <div>
                  <dt class="text-sm font-medium text-gray-500">Company Name</dt>
                  <dd class="mt-1 text-sm text-gray-900">
                    {currentSubscription.company_name || 'Not provided'}
                  </dd>
                </div>
                
                <div>
                  <dt class="text-sm font-medium text-gray-500">Tax ID</dt>
                  <dd class="mt-1 text-sm text-gray-900">
                    {currentSubscription.tax_id || 'Not provided'}
                  </dd>
                </div>
                
                <div>
                  <dt class="text-sm font-medium text-gray-500">Billing Address</dt>
                  <dd class="mt-1 text-sm text-gray-900">
                    {currentSubscription.billing_address || 'Not provided'}
                  </dd>
                </div>
              </dl>
              
              <div class="mt-4 pt-4 border-t border-gray-200">
                <Button variant="outline" size="sm">
                  Update Billing Information
                </Button>
              </div>
            </Card>
          {:else}
            <Alert type="info">
              You don't have an active subscription. Choose a plan to get started.
            </Alert>
            
            <div class="text-center">
              <Button on:click={() => activeTab = 'plans'}>
                View Plans
              </Button>
            </div>
          {/if}
        </div>
      {:else if activeTab === 'plans'}
        <!-- Plans Tab -->
        <div>
          {#if currentSubscription}
            <Alert type="info" class="mb-6">
              You are currently on the <strong>{currentSubscription.plan.name}</strong> plan.
              {#if currentSubscription.status === 'trial'}
                Your trial ends on {new Date(currentSubscription.trial_end).toLocaleDateString()}.
              {/if}
            </Alert>
          {/if}
          
          <PricingTable
            {plans}
            currentPlanId={currentSubscription?.plan.id}
            on:selectPlan={handlePlanSelect}
          />
        </div>
      {:else if activeTab === 'invoices'}
        <!-- Invoices Tab -->
        <Card title="Billing History">
          {#if invoices.length === 0}
            <div class="text-center py-8">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p class="mt-2 text-sm text-gray-600">No invoices yet</p>
            </div>
          {:else}
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Invoice
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Amount
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th class="relative px-6 py-3">
                      <span class="sr-only">Actions</span>
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  {#each invoices as invoice}
                    <tr>
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        #{invoice.number}
                      </td>
                      
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(invoice.created_at).toLocaleDateString()}
                      </td>
                      
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ${invoice.amount}
                      </td>
                      
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                          {invoice.status === 'paid' ? 'bg-green-100 text-green-800' : ''}
                          {invoice.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : ''}
                          {invoice.status === 'failed' ? 'bg-red-100 text-red-800' : ''}
                        ">
                          {invoice.status}
                        </span>
                      </td>
                      
                      <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <Button
                          size="sm"
                          variant="outline"
                          on:click={() => downloadInvoice(invoice.id)}
                        >
                          Download
                        </Button>
                      </td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          {/if}
        </Card>
      {/if}
    </div>
  </div>