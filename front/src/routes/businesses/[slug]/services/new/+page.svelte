<!-- src/routes/businesses/[slug]/services/new/+page.svelte -->
<script>
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { businessAPI } from '$lib/api/businesses';
    import { servicesAPI } from '$lib/api/services';
    import ServiceForm from '$lib/components/business/ServiceForm.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import toast from 'svelte-french-toast';
    
    const slug = $page.params.slug;
    
    let business = null;
    let loading = true;
    let saving = false;
    
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
    
    async function handleSubmit(serviceData) {
      saving = true;
      
      const { data, error } = await servicesAPI.create({
        ...serviceData,
        business: business.id
      });
      
      if (data) {
        toast.success('Service created successfully!');
        goto(`/businesses/${slug}/services`);
      } else {
        toast.error(error || 'Failed to create service');
      }
      
      saving = false;
    }
    
    function handleCancel() {
      goto(`/businesses/${slug}/services`);
    }
  </script>
  
  {#if loading}
    <div class="min-h-screen flex items-center justify-center">
      <Spinner size="lg">Loading business...</Spinner>
    </div>
  {:else}
    <div class="min-h-screen bg-gray-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-900">Add New Service</h1>
          <p class="mt-2 text-gray-600">
            Create a new service for {business?.name}
          </p>
        </div>
        
        <ServiceForm
          businessId={business?.id}
          on:submit={(e) => handleSubmit(e.detail)}
          on:cancel={handleCancel}
          loading={saving}
        />
      </div>
    </div>
  {/if}