<!-- src/routes/businesses/[slug]/edit/+page.svelte -->
<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { businessAPI } from '$lib/api/businesses';
    import BusinessForm from '$lib/components/business/BusinessForm.svelte';
    import BusinessHours from '$lib/components/business/BusinessHours.svelte';
    import QRCode from '$lib/components/business/QRCode.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Alert from '$lib/components/common/Alert.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import toast from 'svelte-french-toast';
    
    const slug = $page.params.slug;
    
    let business = null;
    let loading = true;
    let saving = false;
    let activeTab = 'general';
    let showDeleteModal = false;
    let deleteConfirmation = '';
    
    onMount(async () => {
      await loadBusiness();
    });
    
    async function loadBusiness() {
      loading = true;
      const { data, error } = await businessAPI.getBySlug(slug);
      
      if (data) {
        business = data;
      } else {
        toast.error('Business not found');
        goto('/dashboard');
      }
      
      loading = false;
    }
    
    async function handleSave(updatedData) {
      saving = true;
      
      const { data, error } = await businessAPI.update(business.id, updatedData);
      
      if (data) {
        business = data;
        toast.success('Business updated successfully');
      } else {
        toast.error(error || 'Failed to update business');
      }
      
      saving = false;
    }
    
    async function handleDelete() {
      if (deleteConfirmation !== business.name) {
        toast.error('Please type the business name to confirm');
        return;
      }
      
      const { data, error } = await businessAPI.delete(business.id);
      
      if (data) {
        toast.success('Business deleted successfully');
        goto('/dashboard');
      } else {
        toast.error(error || 'Failed to delete business');
      }
    }
    
    async function handleStatusToggle() {
      const newStatus = !business.is_active;
      const { data, error } = await businessAPI.update(business.id, {
        is_active: newStatus
      });
      
      if (data) {
        business = data;
        toast.success(`Business ${newStatus ? 'activated' : 'deactivated'} successfully`);
      }
    }
  </script>
  
  {#if loading}
    <div class="min-h-screen flex items-center justify-center">
      <Spinner size="lg">Loading business...</Spinner>
    </div>
  {:else if business}
    <div class="min-h-screen bg-gray-50">
      <!-- Header -->
      <div class="bg-white shadow-sm border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="py-6 flex items-center justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">Edit Business</h1>
              <p class="mt-1 text-sm text-gray-600">
                Manage your business settings and information
              </p>
            </div>
            
            <div class="flex items-center space-x-3">
              <Button
                variant="outline"
                href="/businesses/{slug}"
              >
                View Public Page
              </Button>
              
              <Button
                variant={business.is_active ? 'outline' : 'primary'}
                on:click={handleStatusToggle}
              >
                {business.is_active ? 'Deactivate' : 'Activate'}
              </Button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Tabs -->
      <div class="bg-white border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex space-x-8">
            {#each [
              { id: 'general', label: 'General', icon: 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4' },
              { id: 'hours', label: 'Hours', icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' },
              { id: 'services', label: 'Services', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' },
              { id: 'qrcode', label: 'QR Code', icon: 'M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z' },
              { id: 'danger', label: 'Danger Zone', icon: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z' }
            ] as tab}
              <button
                class="py-4 px-1 border-b-2 font-medium text-sm transition-colors flex items-center
                       {activeTab === tab.id 
                         ? 'border-indigo-500 text-indigo-600' 
                         : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}"
                on:click={() => activeTab = tab.id}
              >
                <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={tab.icon} />
                </svg>
                {tab.label}
              </button>
            {/each}
          </div>
        </div>
      </div>
      
      <!-- Content -->
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {#if activeTab === 'general'}
          <BusinessForm
            {business}
            on:save={(e) => handleSave(e.detail)}
            {saving}
          />
        {:else if activeTab === 'hours'}
          <Card title="Business Hours">
            <BusinessHours
              hours={business.business_hours || []}
              editable={true}
              on:save={(e) => handleSave({ business_hours: e.detail })}
            />
          </Card>
        {:else if activeTab === 'services'}
          <Card>
            <div slot="header" class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900">Services</h3>
              <Button size="sm" href="/businesses/{slug}/services/new">
                Add Service
              </Button>
            </div>
            
            <div class="space-y-4">
              {#if business.services && business.services.length > 0}
                {#each business.services as service}
                  <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 class="font-medium text-gray-900">{service.name}</h4>
                      <p class="text-sm text-gray-600">
                        ${service.price} • {service.duration_minutes} minutes
                      </p>
                    </div>
                    
                    <div class="flex items-center space-x-2">
                      <Button
                        size="sm"
                        variant="outline"
                        href="/businesses/{slug}/services/{service.id}/edit"
                      >
                        Edit
                      </Button>
                      
                      <div class="relative inline-block w-12 mr-2 align-middle select-none">
                        <input
                          type="checkbox"
                          checked={service.is_active}
                          on:change={() => {/* Toggle service status */}}
                          class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                        />
                        <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                      </div>
                    </div>
                  </div>
                {/each}
              {:else}
                <div class="text-center py-8">
                  <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <p class="mt-2 text-gray-600">No services added yet</p>
                  <Button class="mt-4" href="/businesses/{slug}/services/new">
                    Add Your First Service
                  </Button>
                </div>
              {/if}
            </div>
          </Card>
        {:else if activeTab === 'qrcode'}
          <QRCode {business} showCustomization />
        {:else if activeTab === 'danger'}
          <Card title="Danger Zone">
            <Alert type="warning">
              These actions are irreversible. Please proceed with caution.
            </Alert>
            
            <div class="mt-6 space-y-6">
              <!-- Deactivate Business -->
              <div class="flex items-center justify-between p-4 border border-yellow-200 rounded-lg bg-yellow-50">
                <div>
                  <h4 class="font-medium text-gray-900">
                    {business.is_active ? 'Deactivate' : 'Activate'} Business
                  </h4>
                  <p class="text-sm text-gray-600">
                    {business.is_active 
                      ? 'Temporarily hide your business from customers'
                      : 'Make your business visible to customers again'}
                  </p>
                </div>
                
                <Button
                  variant="outline"
                  on:click={handleStatusToggle}
                >
                  {business.is_active ? 'Deactivate' : 'Activate'}
                </Button>
              </div>
              
              <!-- Delete Business -->
              <div class="flex items-center justify-between p-4 border border-red-200 rounded-lg bg-red-50">
                <div>
                  <h4 class="font-medium text-gray-900">Delete Business</h4>
                  <p class="text-sm text-gray-600">
                    Permanently delete this business and all its data
                  </p>
                </div>
                
                <Button
                  variant="danger"
                  on:click={() => showDeleteModal = true}
                >
                  Delete Business
                </Button>
              </div>
            </div>
          </Card>
        {/if}
      </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <Modal bind:open={showDeleteModal} title="Delete Business" size="md">
      <div class="space-y-4">
        <Alert type="error">
          <strong>Warning:</strong> This action cannot be undone. All data associated with this business will be permanently deleted.
        </Alert>
        
        <div>
          <p class="text-sm text-gray-600 mb-2">
            Please type <strong>{business.name}</strong> to confirm deletion:
          </p>
          <input
            type="text"
            bind:value={deleteConfirmation}
            placeholder="Type business name here"
            class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-red-500 focus:ring-red-500"
          />
        </div>
      </div>
      
      <div slot="footer" class="flex justify-end gap-3">
        <Button variant="outline" on:click={() => showDeleteModal = false}>
          Cancel
        </Button>
        <Button
          variant="danger"
          on:click={handleDelete}
          disabled={deleteConfirmation !== business.name}
        >
          Delete Business
        </Button>
      </div>
    </Modal>
  {/if}
  
  <style>
    .toggle-checkbox:checked {
      right: 0;
      border-color: #4f46e5;
    }
    .toggle-checkbox:checked + .toggle-label {
      background-color: #4f46e5;
    }
  </style>