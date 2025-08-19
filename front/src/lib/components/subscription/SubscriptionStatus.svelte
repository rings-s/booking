<!-- src/lib/components/subscription/SubscriptionStatus.svelte -->
<script>
    import { onMount } from 'svelte';
    import { formatDate, formatCurrency } from '$lib/utils/formatters';
    import Button from '../common/Button.svelte';
    import Alert from '../common/Alert.svelte';
    import Card from '../common/Card.svelte';
    import Modal from '../common/Modal.svelte';
    import { subscriptionAPI } from '$lib/api/subscriptions';
    import { goto } from '$app/navigation';
    import toast from 'svelte-french-toast';
    
    let {
        subscription = null,
        usage = null,
        loading = false,
        showActions = true,
        ...restProps
    } = $props();
    
    let cancelModalOpen = false;
    let cancelling = false;
    
    onMount(async () => {
      if (!subscription) {
        await loadSubscription();
      }
      if (!usage) {
        await loadUsage();
      }
    });
    
    async function loadSubscription() {
      loading = true;
      const { data, error } = await subscriptionAPI.getCurrentSubscription();
      
      if (data) {
        subscription = data;
      }
      loading = false;
    }
    
    async function loadUsage() {
      const { data } = await subscriptionAPI.getUsage();
      if (data) {
        usage = data;
      }
    }
    
    async function handleCancel() {
      cancelling = true;
      const { data, error } = await subscriptionAPI.cancelSubscription(subscription.id);
      
      if (data) {
        toast.success('Subscription cancelled successfully');
        subscription = data;
        cancelModalOpen = false;
      } else if (error) {
        toast.error(error);
      }
      
      cancelling = false;
    }
    
    async function handleResume() {
      const { data, error } = await subscriptionAPI.resumeSubscription(subscription.id);
      
      if (data) {
        toast.success('Subscription resumed successfully');
        subscription = data;
      } else if (error) {
        toast.error(error);
      }
    }
    
    function handleUpgrade() {
      goto('/subscriptions/upgrade');
    }
    
    function handleManageBilling() {
      goto('/subscriptions/billing');
    }
    
    // Calculate days until renewal/expiry
    let daysUntilRenewal = $derived(subscription?.current_period_end 
      ? Math.ceil((new Date(subscription.current_period_end) - new Date()) / (1000 * 60 * 60 * 24))
      : 0);
    
    let isExpiringSoon = $derived(daysUntilRenewal > 0 && daysUntilRenewal <= 7);
    let isExpired = $derived(subscription?.status === 'expired' || daysUntilRenewal < 0);
    
    // Usage percentages
    let bookingsUsagePercent = $derived(usage && subscription?.plan
      ? (usage.bookings_count / subscription.plan.max_bookings_per_month) * 100
      : 0);
    
    let servicesUsagePercent = $derived(usage && subscription?.plan
      ? (usage.services_count / subscription.plan.max_services) * 100
      : 0);
    
    let staffUsagePercent = $derived(usage && subscription?.plan
      ? (usage.staff_count / subscription.plan.max_staff_accounts) * 100
      : 0);
  </script>
  
  <Card {header}>
    {#snippet header()}
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">Subscription Status</h3>
        {#if showActions && subscription}
          <Button variant="outline" size="sm" on:click={handleManageBilling}>
            Manage Billing
          </Button>
        {/if}
      </div>
    {/snippet}
    
    {#if loading}
      <div class="animate-pulse space-y-4">
        <div class="h-4 bg-gray-200 rounded w-3/4"></div>
        <div class="h-4 bg-gray-200 rounded w-1/2"></div>
        <div class="h-4 bg-gray-200 rounded w-2/3"></div>
      </div>
    {:else if subscription}
      <!-- Alerts -->
      {#if isExpiringSoon && subscription.status === 'active'}
        <Alert type="warning" dismissible class="mb-4">
          Your subscription will expire in {daysUntilRenewal} days. Please renew to continue using our services.
        </Alert>
      {/if}
      
      {#if isExpired}
        <Alert type="error" class="mb-4">
          Your subscription has expired. Please upgrade to continue using our services.
        </Alert>
      {/if}
      
      {#if subscription.status === 'trial'}
        <Alert type="info" class="mb-4">
          You are currently on a free trial. Your trial ends on {formatDate(subscription.trial_end)}.
        </Alert>
      {/if}
      
      <!-- Plan Details -->
      <div class="space-y-4">
        <div class="bg-gray-50 rounded-lg p-4">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h4 class="text-lg font-semibold text-gray-900 capitalize">
                {subscription.plan?.name || 'Unknown'} Plan
              </h4>
              <p class="text-sm text-gray-500">
                {subscription.plan?.price ? formatCurrency(subscription.plan.price) : 'N/A'}/month
              </p>
            </div>
            
            <span class="
              inline-flex items-center px-3 py-1 rounded-full text-sm font-medium
              {subscription.status === 'active' ? 'bg-green-100 text-green-800' : ''}
              {subscription.status === 'trial' ? 'bg-blue-100 text-blue-800' : ''}
              {subscription.status === 'cancelled' ? 'bg-red-100 text-red-800' : ''}
              {subscription.status === 'expired' ? 'bg-gray-100 text-gray-800' : ''}
            ">
              {subscription.status}
            </span>
          </div>
          
          <dl class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <dt class="text-gray-500">Customer Since</dt>
              <dd class="font-medium text-gray-900">{formatDate(subscription.created_at)}</dd>
            </div>
            
            <div>
              <dt class="text-gray-500">Next Billing Date</dt>
              <dd class="font-medium text-gray-900">
                {subscription.status === 'cancelled' 
                  ? 'Cancelled' 
                  : formatDate(subscription.current_period_end)}
              </dd>
            </div>
            
            {#if subscription.trial_end}
              <div>
                <dt class="text-gray-500">Trial Ends</dt>
                <dd class="font-medium text-gray-900">{formatDate(subscription.trial_end)}</dd>
              </div>
            {/if}
            
            {#if subscription.stripe_subscription_id}
              <div>
                <dt class="text-gray-500">Subscription ID</dt>
                <dd class="font-mono text-xs text-gray-600">
                  {subscription.stripe_subscription_id.slice(0, 20)}...
                </dd>
              </div>
            {/if}
          </dl>
        </div>
        
        <!-- Usage Stats -->
        {#if usage}
          <div>
            <h4 class="text-sm font-medium text-gray-900 mb-3">Usage This Month</h4>
            
            <div class="space-y-3">
              <!-- Bookings Usage -->
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600">Bookings</span>
                  <span class="font-medium text-gray-900">
                    {usage.bookings_count || 0} / {subscription.plan?.max_bookings_per_month === -1 ? '∞' : (subscription.plan?.max_bookings_per_month || 'N/A')}
                  </span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300 {bookingsUsagePercent >= 90 ? 'bg-red-500' : bookingsUsagePercent >= 75 ? 'bg-yellow-500' : 'bg-green-500'}"
                    style="width: {Math.min(bookingsUsagePercent, 100)}%"
                  ></div>
                </div>
              </div>
              
              <!-- Services Usage -->
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600">Services</span>
                  <span class="font-medium text-gray-900">
                    {usage.services_count || 0} / {subscription.plan?.max_services === -1 ? '∞' : (subscription.plan?.max_services || 'N/A')}
                  </span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300 {servicesUsagePercent >= 90 ? 'bg-red-500' : servicesUsagePercent >= 75 ? 'bg-yellow-500' : 'bg-green-500'}"
                    style="width: {Math.min(servicesUsagePercent, 100)}%"
                  ></div>
                </div>
              </div>
              
              <!-- Staff Usage -->
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-600">Staff Accounts</span>
                  <span class="font-medium text-gray-900">
                    {usage.staff_count || 1} / {subscription.plan?.max_staff_accounts === -1 ? '∞' : (subscription.plan?.max_staff_accounts || 'N/A')}
                  </span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300 {staffUsagePercent >= 90 ? 'bg-red-500' : staffUsagePercent >= 75 ? 'bg-yellow-500' : 'bg-green-500'}"
                    style="width: {Math.min(staffUsagePercent, 100)}%"
                  ></div>
                </div>
              </div>
            </div>
            
            {#if bookingsUsagePercent >= 90 || servicesUsagePercent >= 90}
              <Alert type="warning" class="mt-3">
                You're approaching your plan limits. Consider upgrading for more capacity.
              </Alert>
            {/if}
          </div>
        {/if}
        
        <!-- Actions -->
        {#if showActions}
          <div class="flex flex-wrap gap-3 pt-4 border-t border-gray-200">
            {#if subscription.status === 'active' || subscription.status === 'trial'}
              <Button on:click={handleUpgrade}>
                Upgrade Plan
              </Button>
              
              <Button variant="outline" href="/subscriptions/invoices">
                View Invoices
              </Button>
              
              {#if subscription.status === 'active'}
                <Button variant="outline" on:click={() => cancelModalOpen = true}>
                  Cancel Subscription
                </Button>
              {/if}
            {:else if subscription.status === 'cancelled'}
              <Button on:click={handleResume}>
                Resume Subscription
              </Button>
              
              <Button variant="outline" on:click={handleUpgrade}>
                Choose New Plan
              </Button>
            {:else if subscription.status === 'expired'}
              <Button on:click={handleUpgrade}>
                Reactivate Subscription
              </Button>
            {/if}
          </div>
        {/if}
      </div>
    {:else}
      <!-- No Subscription -->
      <div class="text-center py-8">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No Active Subscription</h3>
        <p class="mt-1 text-sm text-gray-500">Choose a plan to get started</p>
        <div class="mt-6">
          <Button href="/subscriptions">View Plans</Button>
        </div>
      </div>
    {/if}
  </Card>
  
  <!-- Cancel Confirmation Modal -->
  {#if cancelModalOpen}
    <Modal bind:open={cancelModalOpen} title="Cancel Subscription" {footer}>
      <div class="space-y-4">
        <Alert type="warning">
          Are you sure you want to cancel your subscription? You'll lose access to premium features at the end of your billing period.
        </Alert>
        
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="text-sm font-medium text-gray-900 mb-2">What happens when you cancel:</h4>
          <ul class="text-sm text-gray-600 space-y-1">
            <li>• Your subscription remains active until {formatDate(subscription.current_period_end)}</li>
            <li>• You won't be charged again</li>
            <li>• You'll lose access to premium features after the billing period ends</li>
            <li>• Your data will be preserved for 30 days</li>
            <li>• You can reactivate anytime</li>
          </ul>
        </div>
      </div>
      
      {#snippet footer()}
        <div class="flex justify-end gap-3">
          <Button variant="outline" on:click={() => cancelModalOpen = false}>
            Keep Subscription
          </Button>
          <Button variant="danger" on:click={handleCancel} loading={cancelling}>
            Cancel Subscription
          </Button>
        </div>
      {/snippet}
    </Modal>
  {/if}