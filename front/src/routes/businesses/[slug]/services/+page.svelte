<!-- src/routes/businesses/[slug]/services/+page.svelte -->
<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { businessAPI } from '$lib/api/businesses';
    import { serviceAPI } from '$lib/api/services';
    import Button from '$lib/components/common/Button.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Alert from '$lib/components/common/Alert.svelte';
    import Modal from '$lib/components/common/Modal.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import Select from '$lib/components/common/Select.svelte';
    import toast from 'svelte-french-toast';
    import { flip } from 'svelte/animate';
    import { dndzone } from 'svelte-dnd-action';
    
    const slug = $page.params.slug;
    
    let business = null;
    let services = [];
    let loading = true;
    let selectedService = null;
    let showDeleteModal = false;
    let filterCategory = '';
    let sortBy = 'order';
    let reordering = false;
    
    const sortOptions = [
      { value: 'order', label: 'Custom Order' },
      { value: 'name', label: 'Name (A-Z)' },
      { value: 'price_low', label: 'Price: Low to High' },
      { value: 'price_high', label: 'Price: High to Low' },
      { value: 'duration', label: 'Duration' },
      { value: 'bookings', label: 'Most Booked' }
    ];
    
    onMount(async () => {
      await loadBusiness();
      await loadServices();
    });
    
    async function loadBusiness() {
      const { data, error } = await businessAPI.getBySlug(slug);
      
      if (data) {
        business = data;
      } else {
        toast.error('Business not found');
        goto('/dashboard');
      }
    }
    
    async function loadServices() {
      loading = true;
      
      const { data, error } = await businessAPI.getServices(slug);
      
      if (data) {
        services = sortServices(data);
      }
      
      loading = false;
    }
    
    function sortServices(servicesList) {
      const sorted = [...servicesList];
      
      switch (sortBy) {
        case 'name':
          return sorted.sort((a, b) => a.name.localeCompare(b.name));
        case 'price_low':
          return sorted.sort((a, b) => a.price - b.price);
        case 'price_high':
          return sorted.sort((a, b) => b.price - a.price);
        case 'duration':
          return sorted.sort((a, b) => a.duration_minutes - b.duration_minutes);
        case 'bookings':
          return sorted.sort((a, b) => (b.booking_count || 0) - (a.booking_count || 0));
        default:
          return sorted.sort((a, b) => (a.display_order || 0) - (b.display_order || 0));
      }
    }
    
    async function handleToggleStatus(service) {
      const { data, error } = await serviceAPI.update(service.id, {
        is_active: !service.is_active
      });
      
      if (data) {
        const index = services.findIndex(s => s.id === service.id);
        services[index] = data;
        toast.success(`Service ${data.is_active ? 'activated' : 'deactivated'}`);
      }
    }
    
    async function handleDelete() {
      if (!selectedService) return;
      
      const { data, error } = await serviceAPI.delete(selectedService.id);
      
      if (data) {
        services = services.filter(s => s.id !== selectedService.id);
        showDeleteModal = false;
        selectedService = null;
        toast.success('Service deleted successfully');
      } else {
        toast.error(error || 'Failed to delete service');
      }
    }
    
    async function handleDuplicate(service) {
      const { data, error } = await serviceAPI.create({
        ...service,
        name: `${service.name} (Copy)`,
        id: undefined
      });
      
      if (data) {
        services = [...services, data];
        toast.success('Service duplicated successfully');
      }
    }
    
    async function handleReorder(e) {
      services = e.detail.items;
      
      // Save new order
      const updates = services.map((service, index) => ({
        id: service.id,
        display_order: index
      }));
      
      const { error } = await serviceAPI.updateOrder(updates);
      
      if (error) {
        toast.error('Failed to save order');
        await loadServices(); // Reload original order
      }
    }
    
    function handleSort() {
      services = sortServices(services);
    }
    
    // Get unique categories
    $: categories = [...new Set(services.map(s => s.category).filter(Boolean))];
    
    // Filter services
    $: filteredServices = filterCategory
      ? services.filter(s => s.category === filterCategory)
      : services;
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Manage Services</h1>
            <p class="mt-1 text-sm text-gray-600">
              {business?.name || 'Loading...'}
            </p>
          </div>
          
          <div class="flex items-center space-x-3">
            <Button variant="outline" href="/businesses/{slug}">
              View Business
            </Button>
            
            <Button href="/businesses/{slug}/services/new">
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Add Service
            </Button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Toolbar -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-white rounded-lg shadow-sm p-4">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="flex items-center space-x-4">
            {#if categories.length > 0}
              <Select
                bind:value={filterCategory}
                options={[
                  { value: '', label: 'All Categories' },
                  ...categories.map(c => ({ value: c, label: c }))
                ]}
              />
            {/if}
            
            <Select
              bind:value={sortBy}
              options={sortOptions}
              on:change={handleSort}
            />
            
            <Button
              variant="outline"
              size="sm"
              on:click={() => reordering = !reordering}
              disabled={sortBy !== 'order'}
            >
              <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
              </svg>
              {reordering ? 'Done Reordering' : 'Reorder'}
            </Button>
          </div>
          
          <div class="text-sm text-gray-600">
            {filteredServices.length} {filteredServices.length === 1 ? 'service' : 'services'}
          </div>
        </div>
      </div>
    </div>
    
    <!-- Services Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      {#if loading}
        <div class="flex justify-center py-12">
          <Spinner size="lg">Loading services...</Spinner>
        </div>
      {:else if filteredServices.length === 0}
        <Card>
          <div class="text-center py-12">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 class="mt-2 text-lg font-medium text-gray-900">No services yet</h3>
            <p class="mt-1 text-sm text-gray-500">Get started by adding your first service</p>
            <div class="mt-6">
              <Button href="/businesses/{slug}/services/new">
                Add Service
              </Button>
            </div>
          </div>
        </Card>
      {:else if reordering && sortBy === 'order'}
        <!-- Drag and Drop Reorder Mode -->
        <div
          use:dndzone={{ items: filteredServices, flipDurationMs: 300 }}
          on:consider={handleReorder}
          on:finalize={handleReorder}
          class="space-y-4"
        >
          {#each filteredServices as service (service.id)}
            <div animate:flip={{ duration: 300 }} class="bg-white rounded-lg shadow-sm p-4 cursor-move">
              <div class="flex items-center">
                <svg class="w-6 h-6 text-gray-400 mr-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
                
                <div class="flex-1">
                  <h3 class="font-medium text-gray-900">{service.name}</h3>
                  <p class="text-sm text-gray-600">
                    ${service.price} • {service.duration_minutes} min
                  </p>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {:else}
        <!-- Normal Grid View -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {#each filteredServices as service}
            <Card>
              <div class="space-y-4">
                <!-- Service Header -->
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <h3 class="text-lg font-semibold text-gray-900">{service.name}</h3>
                    {#if service.category}
                      <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700 mt-1">
                        {service.category}
                      </span>
                    {/if}
                  </div>
                  
                  <div class="relative inline-block w-12 align-middle select-none">
                    <input
                      type="checkbox"
                      checked={service.is_active}
                      on:change={() => handleToggleStatus(service)}
                      class="toggle-checkbox absolute block w-6 h-6 rounded-full bg-white border-4 appearance-none cursor-pointer"
                    />
                    <label class="toggle-label block overflow-hidden h-6 rounded-full bg-gray-300 cursor-pointer"></label>
                  </div>
                </div>
                
                <!-- Service Details -->
                <p class="text-sm text-gray-600 line-clamp-2">{service.description}</p>
                
                <div class="flex items-center justify-between text-sm">
                  <span class="font-semibold text-gray-900">${service.price}</span>
                  <span class="text-gray-600">{service.duration_minutes} minutes</span>
                </div>
                
                {#if service.booking_count}
                  <div class="flex items-center text-sm text-gray-600">
                    <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {service.booking_count} bookings
                  </div>
                {/if}
                
                <!-- Actions -->
                <div class="flex items-center space-x-2 pt-4 border-t border-gray-200">
                  <Button
                    size="sm"
                    variant="outline"
                    href="/businesses/{slug}/services/{service.id}/edit"
                    class="flex-1"
                  >
                    Edit
                  </Button>
                  
                  <Button
                    size="sm"
                    variant="outline"
                    on:click={() => handleDuplicate(service)}
                    class="flex-1"
                  >
                    Duplicate
                  </Button>
                  
                  <Button
                    size="sm"
                    variant="outline"
                    on:click={() => {
                      selectedService = service;
                      showDeleteModal = true;
                    }}
                  >
                    <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </Button>
                </div>
              </div>
            </Card>
          {/each}
        </div>
      {/if}
    </div>
    
    <!-- Delete Confirmation Modal -->
    <Modal bind:open={showDeleteModal} title="Delete Service" size="sm">
      <p class="text-gray-600">
        Are you sure you want to delete <strong>{selectedService?.name}</strong>? 
        This action cannot be undone.
      </p>
      
      <div slot="footer" class="flex justify-end gap-3">
        <Button variant="outline" on:click={() => showDeleteModal = false}>
          Cancel
        </Button>
        <Button variant="danger" on:click={handleDelete}>
          Delete Service
        </Button>
      </div>
    </Modal>
  </div>
  
  <style>
    .toggle-checkbox:checked {
      right: 0;
      border-color: #4f46e5;
    }
    .toggle-checkbox:checked + .toggle-label {
      background-color: #4f46e5;
    }
    
    .line-clamp-2 {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  </style>