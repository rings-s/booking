<!-- src/lib/components/business/BusinessForm.svelte -->
<script>
  import Input from '../common/Input.svelte';
  import Select from '../common/Select.svelte';
  import Button from '../common/Button.svelte';
  import { validateForm, businessSchema } from '$lib/utils/validators';
  import { BUSINESS_CATEGORIES } from '$lib/utils/constants';
  
  let {
    business = {},
    loading = false,
    onsubmit = () => {},
    oncancel = () => {},
    ...restProps
  } = $props();
  
  let formData = $state({
    name: business.name || '',
    email: business.email || '',
    phone: business.phone || '',
    description: business.description || '',
    category: business.category || '',
    website: business.website || '',
    address: business.address || '',
    city: business.city || '',
    state: business.state || '',
    country: business.country || '',
    postal_code: business.postal_code || '',
    accepts_online_bookings: business.accepts_online_bookings ?? true,
    auto_confirm_bookings: business.auto_confirm_bookings ?? false,
    logo: null,
    cover_image: null
  });
  
  // Image previews
  let logoPreview = $state(business.logo || null);
  let coverPreview = $state(business.cover_image || null);
  let logoFileInput = $state();
  let coverFileInput = $state();
  
  let errors = $state({});
  
  // Image handling functions
  function handleLogoChange(event) {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        errors.logo = 'Logo file size must be less than 5MB';
        return;
      }
      
      if (!file.type.startsWith('image/')) {
        errors.logo = 'Logo must be an image file';
        return;
      }
      
      formData.logo = file;
      logoPreview = URL.createObjectURL(file);
      delete errors.logo;
    }
  }
  
  function handleCoverChange(event) {
    const file = event.target.files[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        errors.cover_image = 'Cover image file size must be less than 10MB';
        return;
      }
      
      if (!file.type.startsWith('image/')) {
        errors.cover_image = 'Cover image must be an image file';
        return;
      }
      
      formData.cover_image = file;
      coverPreview = URL.createObjectURL(file);
      delete errors.cover_image;
    }
  }
  
  function removeLogo() {
    formData.logo = null;
    logoPreview = null;
    if (logoFileInput) logoFileInput.value = '';
    delete errors.logo;
  }
  
  function removeCover() {
    formData.cover_image = null;
    coverPreview = null;
    if (coverFileInput) coverFileInput.value = '';
    delete errors.cover_image;
  }
  
  async function handleSubmit() {
    const validation = await validateForm(businessSchema, formData);
    
    if (!validation.isValid) {
      errors = validation.errors;
      return;
    }
    
    errors = {};
    onsubmit(formData);
  }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-6">
  <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
    <div class="sm:col-span-2">
      <Input
        label="Business Name"
        bind:value={formData.name}
        error={errors.name}
        required
      />
    </div>
    
    <!-- Image uploads -->
    <div class="sm:col-span-2">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Business Images</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Logo Upload -->
        <div class="space-y-3">
          <label class="block text-sm font-medium text-gray-700">
            Business Logo
            <span class="text-xs text-gray-500">(Max 5MB)</span>
          </label>
          
          {#if logoPreview}
            <div class="relative">
              <img 
                src={logoPreview} 
                alt="Logo preview" 
                class="w-32 h-32 object-cover border-2 border-gray-200 rounded-lg"
              />
              <button
                type="button"
                on:click={removeLogo}
                class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          {:else}
            <div 
              class="w-32 h-32 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center hover:border-gray-400 cursor-pointer"
              on:click={() => logoFileInput.click()}
              role="button"
              tabindex="0"
            >
              <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </div>
          {/if}
          
          <input
            bind:this={logoFileInput}
            type="file"
            accept="image/*"
            on:change={handleLogoChange}
            class="hidden"
          />
          
          <Button
            type="button"
            variant="outline"
            size="sm"
            on:click={() => logoFileInput.click()}
          >
            {logoPreview ? 'Change Logo' : 'Upload Logo'}
          </Button>
          
          {#if errors.logo}
            <p class="text-sm text-red-600">{errors.logo}</p>
          {/if}
        </div>
        
        <!-- Cover Image Upload -->
        <div class="space-y-3">
          <label class="block text-sm font-medium text-gray-700">
            Cover Image
            <span class="text-xs text-gray-500">(Max 10MB)</span>
          </label>
          
          {#if coverPreview}
            <div class="relative">
              <img 
                src={coverPreview} 
                alt="Cover preview" 
                class="w-full h-32 object-cover border-2 border-gray-200 rounded-lg"
              />
              <button
                type="button"
                on:click={removeCover}
                class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          {:else}
            <div 
              class="w-full h-32 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center hover:border-gray-400 cursor-pointer"
              on:click={() => coverFileInput.click()}
              role="button"
              tabindex="0"
            >
              <div class="text-center">
                <svg class="mx-auto w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p class="text-xs text-gray-500 mt-1">Cover Image</p>
              </div>
            </div>
          {/if}
          
          <input
            bind:this={coverFileInput}
            type="file"
            accept="image/*"
            on:change={handleCoverChange}
            class="hidden"
          />
          
          <Button
            type="button"
            variant="outline"
            size="sm"
            on:click={() => coverFileInput.click()}
          >
            {coverPreview ? 'Change Cover' : 'Upload Cover'}
          </Button>
          
          {#if errors.cover_image}
            <p class="text-sm text-red-600">{errors.cover_image}</p>
          {/if}
        </div>
      </div>
    </div>
    
    <Input
      label="Email"
      type="email"
      bind:value={formData.email}
      error={errors.email}
      required
    />
    
    <Input
      label="Phone"
      type="tel"
      bind:value={formData.phone}
      error={errors.phone}
      required
    />
    
    <Select
      label="Category"
      bind:value={formData.category}
      options={BUSINESS_CATEGORIES}
      error={errors.category}
      required
    />
    
    <Input
      label="Website"
      type="url"
      bind:value={formData.website}
      error={errors.website}
    />
    
    <div class="sm:col-span-2">
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Description
        <span class="text-red-500">*</span>
      </label>
      <textarea
        bind:value={formData.description}
        rows="4"
        class="
          block w-full rounded-md shadow-sm sm:text-sm
          {errors.description 
            ? 'border-red-300 text-red-900 focus:border-red-500 focus:ring-red-500' 
            : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'}
        "
      ></textarea>
      {#if errors.description}
        <p class="mt-1 text-sm text-red-600">{errors.description}</p>
      {/if}
    </div>
    
    <div class="sm:col-span-2">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Address</h3>
    </div>
    
    <div class="sm:col-span-2">
      <Input
        label="Street Address"
        bind:value={formData.address}
        error={errors.address}
        required
      />
    </div>
    
    <Input
      label="City"
      bind:value={formData.city}
      error={errors.city}
      required
    />
    
    <Input
      label="State/Province"
      bind:value={formData.state}
      error={errors.state}
      required
    />
    
    <Input
      label="Country"
      bind:value={formData.country}
      error={errors.country}
      required
    />
    
    <Input
      label="Postal Code"
      bind:value={formData.postal_code}
      error={errors.postal_code}
      required
    />
    
    <div class="sm:col-span-2">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Settings</h3>
    </div>
    
    <div class="sm:col-span-2 space-y-4">
      <label class="flex items-center">
        <input
          type="checkbox"
          bind:checked={formData.accepts_online_bookings}
          class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
        />
        <span class="ml-2 text-sm text-gray-700">Accept online bookings</span>
      </label>
      
      <label class="flex items-center">
        <input
          type="checkbox"
          bind:checked={formData.auto_confirm_bookings}
          class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
        />
        <span class="ml-2 text-sm text-gray-700">Auto-confirm bookings</span>
      </label>
    </div>
  </div>
  
  <div class="flex justify-end space-x-3">
    <Button variant="outline" type="button" on:click={() => oncancel()}>
      Cancel
    </Button>
    <Button type="submit" {loading}>
      {business.id ? 'Update' : 'Create'} Business
    </Button>
  </div>
</form>