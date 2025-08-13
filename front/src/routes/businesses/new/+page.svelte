<!-- src/routes/businesses/new/+page.svelte -->
<script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { businessAPI } from '$lib/api/businesses';
    import { subscriptionAPI } from '$lib/api/subscriptions';
    import { auth } from '$lib/stores/auth';
    import Input from '$lib/components/common/Input.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Alert from '$lib/components/common/Alert.svelte';
    import BusinessHours from '$lib/components/business/BusinessHours.svelte';
    import { validateForm } from '$lib/utils/validators';
    import toast from 'svelte-french-toast';
    
    let currentStep = 1;
    let loading = false;
    let errors = {};
    let canCreateBusiness = true;
    let subscription = null;
    
    // Business data
    let businessData = {
      name: '',
      slug: '',
      description: '',
      business_type: '',
      phone: '',
      email: '',
      website: '',
      address: '',
      city: '',
      state: '',
      zip_code: '',
      country: 'US',
      timezone: 'America/New_York',
      currency: 'USD',
      tax_rate: 0,
      booking_buffer_hours: 24,
      cancellation_policy_hours: 24,
      auto_confirm_bookings: false,
      require_deposit: false,
      deposit_percentage: 20,
      logo: null,
      cover_image: null
    };
    
    let businessHours = [];
    let amenities = [];
    let socialLinks = {
      facebook: '',
      instagram: '',
      twitter: '',
      linkedin: '',
      youtube: ''
    };
    
    const businessTypes = [
      { value: 'salon', label: 'Salon & Beauty' },
      { value: 'spa', label: 'Spa & Wellness' },
      { value: 'fitness', label: 'Fitness & Gym' },
      { value: 'healthcare', label: 'Healthcare' },
      { value: 'education', label: 'Education & Tutoring' },
      { value: 'professional', label: 'Professional Services' },
      { value: 'automotive', label: 'Automotive' },
      { value: 'home_services', label: 'Home Services' },
      { value: 'other', label: 'Other' }
    ];
    
    const timezones = [
      { value: 'America/New_York', label: 'Eastern Time (ET)' },
      { value: 'America/Chicago', label: 'Central Time (CT)' },
      { value: 'America/Denver', label: 'Mountain Time (MT)' },
      { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
      { value: 'America/Phoenix', label: 'Arizona Time (AZ)' },
      { value: 'Pacific/Honolulu', label: 'Hawaii Time (HT)' }
    ];
    
    const popularAmenities = [
      'Free WiFi',
      'Parking',
      'Wheelchair Accessible',
      'Air Conditioning',
      'Online Booking',
      'Credit Cards Accepted',
      'Walk-ins Welcome',
      'By Appointment Only',
      'Gift Cards Available',
      'Loyalty Program'
    ];
    
    // Check subscription limits on mount
    onMount(async () => {
      const { data } = await subscriptionAPI.getCurrentSubscription();
      if (data) {
        subscription = data;
        const usage = await subscriptionAPI.getUsage();
        if (usage.data) {
          canCreateBusiness = usage.data.businesses_count < subscription.plan.max_businesses;
          if (!canCreateBusiness) {
            toast.error('You have reached your business limit. Please upgrade your plan.');
          }
        }
      }
    });
    
    // Auto-generate slug from business name
    $: if (businessData.name && !businessData.slug) {
      businessData.slug = businessData.name
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '');
    }
    
    async function handleNext() {
      errors = {};
      
      if (currentStep === 1) {
        // Validate basic info
        if (!businessData.name) errors.name = 'Business name is required';
        if (!businessData.business_type) errors.business_type = 'Business type is required';
        if (!businessData.description) errors.description = 'Description is required';
        
        if (Object.keys(errors).length === 0) {
          // Check if slug is available
          const { data } = await businessAPI.checkSlug(businessData.slug);
          if (!data.available) {
            errors.slug = 'This URL is already taken';
          } else {
            currentStep = 2;
          }
        }
      } else if (currentStep === 2) {
        // Validate contact info
        if (!businessData.phone) errors.phone = 'Phone number is required';
        if (!businessData.email) errors.email = 'Email is required';
        if (!businessData.address) errors.address = 'Address is required';
        if (!businessData.city) errors.city = 'City is required';
        if (!businessData.state) errors.state = 'State is required';
        
        if (Object.keys(errors).length === 0) {
          currentStep = 3;
        }
      } else if (currentStep === 3) {
        currentStep = 4;
      } else if (currentStep === 4) {
        await handleSubmit();
      }
    }
    
    async function handleSubmit() {
      loading = true;
      
      const formData = new FormData();
      
      // Add all business data
      Object.keys(businessData).forEach(key => {
        if (businessData[key] !== null && businessData[key] !== '') {
          formData.append(key, businessData[key]);
        }
      });
      
      // Add business hours
      formData.append('business_hours', JSON.stringify(businessHours));
      
      // Add amenities
      formData.append('amenities', JSON.stringify(amenities));
      
      // Add social links
      formData.append('social_links', JSON.stringify(socialLinks));
      
      const { data, error } = await businessAPI.create(formData);
      
      if (data) {
        toast.success('Business created successfully!');
        goto(`/businesses/${data.slug}/services/new`);
      } else {
        errors.general = error || 'Failed to create business';
      }
      
      loading = false;
    }
    
    function handleBack() {
      if (currentStep > 1) {
        currentStep--;
      }
    }
    
    async function handleLogoUpload(event) {
      const file = event.target.files[0];
      if (file) {
        if (file.size > 5 * 1024 * 1024) {
          toast.error('Logo must be less than 5MB');
          return;
        }
        businessData.logo = file;
      }
    }
    
    async function handleCoverUpload(event) {
      const file = event.target.files[0];
      if (file) {
        if (file.size > 10 * 1024 * 1024) {
          toast.error('Cover image must be less than 10MB');
          return;
        }
        businessData.cover_image = file;
      }
    }
    
    function toggleAmenity(amenity) {
      if (amenities.includes(amenity)) {
        amenities = amenities.filter(a => a !== amenity);
      } else {
        amenities = [...amenities, amenity];
      }
    }
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Create Your Business</h1>
        <p class="mt-2 text-gray-600">Set up your business profile in just a few steps</p>
      </div>
      
      <!-- Progress Bar -->
      <div class="mb-8">
        <div class="flex items-center justify-center">
          {#each ['Basic Info', 'Contact', 'Hours', 'Settings'] as step, i}
            <div class="flex items-center">
              <div class="relative">
                <div class="
                  w-12 h-12 rounded-full flex items-center justify-center text-sm font-medium
                  {currentStep > i + 1 
                    ? 'bg-indigo-600 text-white' 
                    : currentStep === i + 1
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-200 text-gray-500'}
                ">
                  {#if currentStep > i + 1}
                    <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  {:else}
                    {i + 1}
                  {/if}
                </div>
                <div class="absolute -bottom-6 left-1/2 transform -translate-x-1/2 text-xs text-gray-600 whitespace-nowrap">
                  {step}
                </div>
              </div>
              {#if i < 3}
                <div class="w-24 h-1 {currentStep > i + 1 ? 'bg-indigo-600' : 'bg-gray-200'}"></div>
              {/if}
            </div>
          {/each}
        </div>
      </div>
      
      <!-- Error Alert -->
      {#if errors.general}
        <Alert type="error" dismissible on:dismiss={() => errors.general = null}>
          {errors.general}
        </Alert>
      {/if}
      
      <!-- Form Content -->
      <div class="mt-12">
        {#if !canCreateBusiness}
          <Card>
            <div class="text-center py-8">
              <svg class="mx-auto h-12 w-12 text-yellow-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <h3 class="text-lg font-medium text-gray-900 mb-2">Business Limit Reached</h3>
              <p class="text-gray-600 mb-6">
                You've reached the maximum number of businesses for your current plan.
              </p>
              <Button href="/subscriptions/upgrade">
                Upgrade Plan
              </Button>
            </div>
          </Card>
        {:else if currentStep === 1}
          <!-- Step 1: Basic Information -->
          <Card title="Basic Information">
            <div class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <Input
                    label="Business Name"
                    bind:value={businessData.name}
                    error={errors.name}
                    placeholder="Acme Services"
                    required
                  />
                  <p class="mt-1 text-xs text-gray-500">This will be displayed to customers</p>
                </div>
                
                <div>
                  <Input
                    label="URL Slug"
                    bind:value={businessData.slug}
                    error={errors.slug}
                    placeholder="acme-services"
                    required
                  />
                  <p class="mt-1 text-xs text-gray-500">
                    Your booking page: bookingpro.com/book/{businessData.slug || 'your-business'}
                  </p>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Business Type <span class="text-red-500">*</span>
                </label>
                <select
                  bind:value={businessData.business_type}
                  class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                >
                  <option value="">Select a type</option>
                  {#each businessTypes as type}
                    <option value={type.value}>{type.label}</option>
                  {/each}
                </select>
                {#if errors.business_type}
                  <p class="mt-1 text-sm text-red-600">{errors.business_type}</p>
                {/if}
              </div>
              
              <div>
                <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
                  Description <span class="text-red-500">*</span>
                </label>
                <textarea
                  id="description"
                  bind:value={businessData.description}
                  rows="4"
                  class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  placeholder="Tell customers what makes your business special..."
                ></textarea>
                {#if errors.description}
                  <p class="mt-1 text-sm text-red-600">{errors.description}</p>
                {/if}
                <p class="mt-1 text-xs text-gray-500">
                  {businessData.description.length}/500 characters
                </p>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Logo
                  </label>
                  <div class="flex items-center space-x-4">
                    {#if businessData.logo}
                      <img 
                        src={URL.createObjectURL(businessData.logo)} 
                        alt="Logo preview"
                        class="w-20 h-20 rounded-lg object-cover"
                      />
                    {:else}
                      <div class="w-20 h-20 rounded-lg bg-gray-200 flex items-center justify-center">
                        <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </div>
                    {/if}
                    
                    <label class="cursor-pointer">
                      <input
                        type="file"
                        accept="image/*"
                        on:change={handleLogoUpload}
                        class="hidden"
                      />
                      <Button variant="outline" size="sm">
                        {businessData.logo ? 'Change' : 'Upload'} Logo
                      </Button>
                    </label>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    Cover Image
                  </label>
                  <div class="flex items-center space-x-4">
                    {#if businessData.cover_image}
                      <img 
                        src={URL.createObjectURL(businessData.cover_image)} 
                        alt="Cover preview"
                        class="w-20 h-20 rounded-lg object-cover"
                      />
                    {:else}
                      <div class="w-20 h-20 rounded-lg bg-gray-200 flex items-center justify-center">
                        <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </div>
                    {/if}
                    
                    <label class="cursor-pointer">
                      <input
                        type="file"
                        accept="image/*"
                        on:change={handleCoverUpload}
                        class="hidden"
                      />
                      <Button variant="outline" size="sm">
                        {businessData.cover_image ? 'Change' : 'Upload'} Cover
                      </Button>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        {:else if currentStep === 2}
          <!-- Step 2: Contact Information -->
          <Card title="Contact Information">
            <div class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Input
                  type="tel"
                  label="Phone Number"
                  bind:value={businessData.phone}
                  error={errors.phone}
                  placeholder="+1 (555) 123-4567"
                  required
                />
                
                <Input
                  type="email"
                  label="Email Address"
                  bind:value={businessData.email}
                  error={errors.email}
                  placeholder="contact@business.com"
                  required
                />
              </div>
              
              <Input
                label="Website"
                bind:value={businessData.website}
                placeholder="https://www.example.com"
              />
              
              <div class="border-t border-gray-200 pt-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Business Address</h3>
                
                <div class="space-y-4">
                  <Input
                    label="Street Address"
                    bind:value={businessData.address}
                    error={errors.address}
                    placeholder="123 Main Street"
                    required
                  />
                  
                  <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <Input
                      label="City"
                      bind:value={businessData.city}
                      error={errors.city}
                      placeholder="New York"
                      required
                    />
                    
                    <Input
                      label="State"
                      bind:value={businessData.state}
                      error={errors.state}
                      placeholder="NY"
                      required
                    />
                    
                    <Input
                      label="ZIP Code"
                      bind:value={businessData.zip_code}
                      placeholder="10001"
                    />
                  </div>
                </div>
              </div>
              
              <div class="border-t border-gray-200 pt-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Social Media (Optional)</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Input
                    label="Facebook"
                    bind:value={socialLinks.facebook}
                    placeholder="https://facebook.com/yourbusiness"
                  />
                  
                  <Input
                    label="Instagram"
                    bind:value={socialLinks.instagram}
                    placeholder="@yourbusiness"
                  />
                  
                  <Input
                    label="Twitter"
                    bind:value={socialLinks.twitter}
                    placeholder="@yourbusiness"
                  />
                  
                  <Input
                    label="LinkedIn"
                    bind:value={socialLinks.linkedin}
                    placeholder="https://linkedin.com/company/yourbusiness"
                  />
                </div>
              </div>
            </div>
          </Card>
        {:else if currentStep === 3}
          <!-- Step 3: Business Hours -->
          <Card title="Business Hours">
            <p class="text-sm text-gray-600 mb-6">
              Set your regular business hours. You can always adjust these later or set special hours for holidays.
            </p>
            
            <BusinessHours
              bind:hours={businessHours}
              editable={true}
            />
            
            <div class="mt-6 border-t border-gray-200 pt-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Amenities & Features</h3>
              <p class="text-sm text-gray-600 mb-4">Select all that apply to help customers find you</p>
              
              <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
                {#each popularAmenities as amenity}
                  <label class="flex items-center p-3 rounded-lg border cursor-pointer hover:bg-gray-50
                    {amenities.includes(amenity) ? 'border-indigo-600 bg-indigo-50' : 'border-gray-200'}">
                    <input
                      type="checkbox"
                      checked={amenities.includes(amenity)}
                      on:change={() => toggleAmenity(amenity)}
                      class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    />
                    <span class="ml-2 text-sm text-gray-700">{amenity}</span>
                  </label>
                {/each}
              </div>
            </div>
          </Card>
        {:else if currentStep === 4}
          <!-- Step 4: Business Settings -->
          <Card title="Business Settings">
            <div class="space-y-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Timezone
                  </label>
                  <select
                    bind:value={businessData.timezone}
                    class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  >
                    {#each timezones as tz}
                      <option value={tz.value}>{tz.label}</option>
                    {/each}
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Currency
                  </label>
                  <select
                    bind:value={businessData.currency}
                    class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  >
                    <option value="USD">USD - US Dollar</option>
                    <option value="EUR">EUR - Euro</option>
                    <option value="GBP">GBP - British Pound</option>
                    <option value="CAD">CAD - Canadian Dollar</option>
                  </select>
                </div>
              </div>
              
              <div class="border-t border-gray-200 pt-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Booking Settings</h3>
                
                <div class="space-y-4">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        Booking Buffer Time
                      </label>
                      <select
                        bind:value={businessData.booking_buffer_hours}
                        class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      >
                        <option value={0}>No buffer</option>
                        <option value={1}>1 hour</option>
                        <option value={2}>2 hours</option>
                        <option value={4}>4 hours</option>
                        <option value={12}>12 hours</option>
                        <option value={24}>24 hours</option>
                        <option value={48}>48 hours</option>
                      </select>
                      <p class="mt-1 text-xs text-gray-500">
                        How far in advance customers must book
                      </p>
                    </div>
                    
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">
                        Cancellation Policy
                      </label>
                      <select
                        bind:value={businessData.cancellation_policy_hours}
                        class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                      >
                        <option value={0}>No restrictions</option>
                        <option value={1}>1 hour before</option>
                        <option value={2}>2 hours before</option>
                        <option value={4}>4 hours before</option>
                        <option value={12}>12 hours before</option>
                        <option value={24}>24 hours before</option>
                        <option value={48}>48 hours before</option>
                      </select>
                      <p class="mt-1 text-xs text-gray-500">
                        Free cancellation window
                      </p>
                    </div>
                  </div>
                  
                  <div class="space-y-3">
                    <label class="flex items-center">
                      <input
                        type="checkbox"
                        bind:checked={businessData.auto_confirm_bookings}
                        class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                      />
                      <span class="ml-2 text-sm text-gray-700">
                        Auto-confirm bookings
                      </span>
                    </label>
                    
                    <label class="flex items-center">
                      <input
                        type="checkbox"
                        bind:checked={businessData.require_deposit}
                        class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                      />
                      <span class="ml-2 text-sm text-gray-700">
                        Require deposit for bookings
                      </span>
                    </label>
                    
                    {#if businessData.require_deposit}
                      <div class="ml-6">
                        <Input
                          type="number"
                          label="Deposit Percentage"
                          bind:value={businessData.deposit_percentage}
                          min="5"
                          max="100"
                          placeholder="20"
                        />
                      </div>
                    {/if}
                  </div>
                </div>
              </div>
              
              <div class="border-t border-gray-200 pt-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Tax Settings</h3>
                
                <Input
                  type="number"
                  label="Tax Rate (%)"
                  bind:value={businessData.tax_rate}
                  min="0"
                  max="100"
                  step="0.01"
                  placeholder="0"
                />
                <p class="mt-1 text-xs text-gray-500">
                  This will be applied to all services unless specified otherwise
                </p>
              </div>
            </div>
          </Card>
        {/if}
        
        <!-- Navigation Buttons -->
        <div class="flex justify-between mt-8">
          {#if currentStep > 1}
            <Button variant="outline" on:click={handleBack}>
              Back
            </Button>
          {:else}
            <div></div>
          {/if}
          
          <div class="flex gap-3">
            <Button variant="outline" href="/dashboard">
              Cancel
            </Button>
            
            <Button on:click={handleNext} {loading}>
              {#if currentStep === 4}
                Create Business
              {:else}
                Next Step
              {/if}
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>