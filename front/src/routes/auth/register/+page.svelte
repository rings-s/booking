<!-- src/routes/auth/register/+page.svelte -->
<script>
    import { goto } from '$app/navigation';
    import { authAPI } from '$lib/api/auth';
    import { auth } from '$lib/stores/auth';
    import Input from '$lib/components/common/Input.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Alert from '$lib/components/common/Alert.svelte';
    import { validateForm, registrationSchema } from '$lib/utils/validators';
    import toast from 'svelte-french-toast';
    
    let currentStep = 1;
    let loading = false;
    let errors = {};
    
    // Step 1: Account Type
    let accountType = ''; // 'customer' or 'business'
    
    // Step 2: Personal Information
    let formData = {
      email: '',
      password: '',
      password_confirm: '',
      first_name: '',
      last_name: '',
      phone: '',
      terms_accepted: false,
      newsletter: false
    };
    
    // Step 3: Business Information (if business account)
    let businessData = {
      business_name: '',
      business_type: '',
      business_phone: '',
      business_email: '',
      address: '',
      city: '',
      state: '',
      zip_code: '',
      country: 'US'
    };
    
    const businessTypes = [
      'Salon & Spa',
      'Healthcare',
      'Fitness & Wellness',
      'Education & Tutoring',
      'Professional Services',
      'Automotive',
      'Home Services',
      'Other'
    ];
    
    async function handleNextStep() {
      errors = {};
      
      if (currentStep === 1) {
        if (!accountType) {
          errors.accountType = 'Please select an account type';
          return;
        }
        currentStep = 2;
      } else if (currentStep === 2) {
        // Validate personal information using Yup
        const { isValid, errors: validationErrors } = await validateForm(registrationSchema, formData);
        errors = validationErrors;
        
        if (isValid) {
          if (accountType === 'business') {
            currentStep = 3;
          } else {
            await handleSubmit();
          }
        }
      } else if (currentStep === 3) {
        // Validate business information
        if (!businessData.business_name) errors.business_name = 'Business name is required';
        if (!businessData.business_type) errors.business_type = 'Business type is required';
        
        if (Object.keys(errors).length === 0) {
          await handleSubmit();
        }
      }
    }
    
    async function handleSubmit() {
      loading = true;
      
      const payload = {
        ...formData,
        account_type: accountType,
        ...(accountType === 'business' ? businessData : {})
      };
      
      const { data, error } = await authAPI.register(payload);
      
      if (data) {
        toast.success('Account created successfully!');
        
        if (accountType === 'business') {
          goto('/dashboard/setup');
        } else {
          goto('/dashboard');
        }
      } else {
        errors.general = error || 'Failed to create account';
        loading = false;
      }
    }
    
    function handleBack() {
      if (currentStep > 1) {
        currentStep--;
      }
    }
  </script>
  
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
    <div class="flex min-h-screen">
      <div class="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-12">
        <div class="max-w-2xl w-full">
          <!-- Header -->
          <div class="text-center mb-8">
            <a href="/" class="inline-flex items-center space-x-2 mb-6">
              <div class="w-12 h-12 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center">
                <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <span class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                BookingPro
              </span>
            </a>
            
            <h2 class="text-3xl font-extrabold text-gray-900">
              Create your account
            </h2>
            <p class="mt-2 text-sm text-gray-600">
              Already have an account?
              <a href="/auth/login" class="font-medium text-indigo-600 hover:text-indigo-500 ml-1">
                Sign in
              </a>
            </p>
          </div>
          
          <!-- Progress Steps -->
          <div class="mb-8">
            <div class="flex items-center justify-center">
              {#each [1, 2, 3] as step}
                {#if step <= (accountType === 'customer' ? 2 : 3)}
                  <div class="flex items-center">
                    <div class="
                      w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium
                      {currentStep >= step 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-gray-200 text-gray-500'}
                    ">
                      {#if currentStep > step}
                        <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                        </svg>
                      {:else}
                        {step}
                      {/if}
                    </div>
                    {#if step < (accountType === 'customer' ? 2 : 3)}
                      <div class="w-16 h-1 {currentStep > step ? 'bg-indigo-600' : 'bg-gray-200'}"></div>
                    {/if}
                  </div>
                {/if}
              {/each}
            </div>
            
            <div class="flex justify-center mt-2 text-xs text-gray-600">
              {#if currentStep === 1}
                Choose Account Type
              {:else if currentStep === 2}
                Personal Information
              {:else if currentStep === 3}
                Business Details
              {/if}
            </div>
          </div>
          
          <!-- Error Alert -->
          {#if errors.general}
            <Alert type="error" dismissible on:dismiss={() => errors.general = null}>
              {errors.general}
            </Alert>
          {/if}
          
          <!-- Form Content -->
          <div class="bg-white rounded-2xl shadow-xl p-8">
            {#if currentStep === 1}
              <!-- Step 1: Account Type -->
              <div class="space-y-6">
                <h3 class="text-xl font-semibold text-gray-900">How will you use BookingPro?</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <button
                    type="button"
                    class="
                      relative p-6 rounded-xl border-2 text-left transition-all
                      {accountType === 'customer' 
                        ? 'border-indigo-600 bg-indigo-50' 
                        : 'border-gray-200 hover:border-gray-300'}
                    "
                    on:click={() => accountType = 'customer'}
                  >
                    {#if accountType === 'customer'}
                      <div class="absolute top-2 right-2">
                        <svg class="w-6 h-6 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                      </div>
                    {/if}
                    
                    <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
                      <svg class="w-6 h-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </div>
                    
                    <h4 class="text-lg font-semibold text-gray-900 mb-2">I'm a Customer</h4>
                    <p class="text-sm text-gray-600">
                      Book services, manage appointments, and discover new businesses
                    </p>
                  </button>
                  
                  <button
                    type="button"
                    class="
                      relative p-6 rounded-xl border-2 text-left transition-all
                      {accountType === 'business' 
                        ? 'border-indigo-600 bg-indigo-50' 
                        : 'border-gray-200 hover:border-gray-300'}
                    "
                    on:click={() => accountType = 'business'}
                  >
                    {#if accountType === 'business'}
                      <div class="absolute top-2 right-2">
                        <svg class="w-6 h-6 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                      </div>
                    {/if}
                    
                    <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                      <svg class="w-6 h-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                    </div>
                    
                    <h4 class="text-lg font-semibold text-gray-900 mb-2">I'm a Business</h4>
                    <p class="text-sm text-gray-600">
                      Manage bookings, grow your customer base, and streamline operations
                    </p>
                  </button>
                </div>
                
                {#if errors.accountType}
                  <p class="text-sm text-red-600 text-center">{errors.accountType}</p>
                {/if}
              </div>
            {:else if currentStep === 2}
              <!-- Step 2: Personal Information -->
              <div class="space-y-4">
                <h3 class="text-xl font-semibold text-gray-900 mb-6">Personal Information</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Input
                    label="First Name"
                    bind:value={formData.first_name}
                    error={errors.first_name}
                    placeholder="John"
                    required
                  />
                  
                  <Input
                    label="Last Name"
                    bind:value={formData.last_name}
                    error={errors.last_name}
                    placeholder="Doe"
                    required
                  />
                </div>
                
                <Input
                  type="email"
                  label="Email Address"
                  bind:value={formData.email}
                  error={errors.email}
                  placeholder="john@example.com"
                  required
                />
                
                <Input
                  type="tel"
                  label="Phone Number"
                  bind:value={formData.phone}
                  error={errors.phone}
                  placeholder="+1 (555) 123-4567"
                />
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Input
                    type="password"
                    label="Password"
                    bind:value={formData.password}
                    error={errors.password}
                    placeholder="••••••••"
                    required
                  />
                  
                  <Input
                    type="password"
                    label="Confirm Password"
                    bind:value={formData.password_confirm}
                    error={errors.password_confirm}
                    placeholder="••••••••"
                    required
                  />
                </div>
                
                <div class="space-y-3 pt-4">
                  <label class="flex items-start">
                    <input
                      type="checkbox"
                      bind:checked={formData.terms_accepted}
                      class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded mt-0.5"
                    />
                    <span class="ml-2 text-sm text-gray-600">
                      I agree to the
                      <a href="/terms" target="_blank" class="text-indigo-600 hover:text-indigo-500">Terms of Service</a>
                      and
                      <a href="/privacy" target="_blank" class="text-indigo-600 hover:text-indigo-500">Privacy Policy</a>
                    </span>
                  </label>
                  
                  <label class="flex items-start">
                    <input
                      type="checkbox"
                      bind:checked={formData.newsletter}
                      class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded mt-0.5"
                    />
                    <span class="ml-2 text-sm text-gray-600">
                      Send me tips, product updates, and special offers
                    </span>
                  </label>
                </div>
                
                {#if errors.terms_accepted}
                  <p class="text-sm text-red-600">{errors.terms_accepted}</p>
                {/if}
              </div>
            {:else if currentStep === 3}
              <!-- Step 3: Business Information -->
              <div class="space-y-4">
                <h3 class="text-xl font-semibold text-gray-900 mb-6">Business Details</h3>
                
                <Input
                  label="Business Name"
                  bind:value={businessData.business_name}
                  error={errors.business_name}
                  placeholder="Acme Services Inc."
                  required
                />
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Business Type <span class="text-red-500">*</span>
                  </label>
                  <select
                    bind:value={businessData.business_type}
                    class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  >
                    <option value="">Select a type</option>
                    {#each businessTypes as type}
                      <option value={type}>{type}</option>
                    {/each}
                  </select>
                  {#if errors.business_type}
                    <p class="mt-1 text-sm text-red-600">{errors.business_type}</p>
                  {/if}
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Input
                    type="email"
                    label="Business Email"
                    bind:value={businessData.business_email}
                    placeholder="contact@business.com"
                  />
                  
                  <Input
                    type="tel"
                    label="Business Phone"
                    bind:value={businessData.business_phone}
                    placeholder="+1 (555) 123-4567"
                  />
                </div>
                
                <Input
                  label="Street Address"
                  bind:value={businessData.address}
                  placeholder="123 Main Street"
                />
                
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
                  <Input
                    label="City"
                    bind:value={businessData.city}
                    placeholder="New York"
                  />
                  
                  <Input
                    label="State"
                    bind:value={businessData.state}
                    placeholder="NY"
                  />
                  
                  <Input
                    label="ZIP Code"
                    bind:value={businessData.zip_code}
                    placeholder="10001"
                  />
                </div>
              </div>
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
              
              <Button on:click={handleNextStep} {loading}>
                {#if currentStep === 1}
                  Continue
                {:else if currentStep === 2 && accountType === 'customer'}
                  Create Account
                {:else if currentStep === 2}
                  Continue
                {:else}
                  Create Business Account
                {/if}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>