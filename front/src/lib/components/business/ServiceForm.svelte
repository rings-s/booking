<!-- src/lib/components/business/ServiceForm.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
    import Input from '../common/Input.svelte';
    import Select from '../common/Select.svelte';
    import Button from '../common/Button.svelte';
    import Card from '../common/Card.svelte';
    import Alert from '../common/Alert.svelte';
    import { validateForm, serviceSchema } from '$lib/utils/validators';
    import { DURATIONS } from '$lib/utils/constants';
    import toast from 'svelte-french-toast';
    
    export let service = {};
    export let businessId;
    export let loading = false;
    
    const dispatch = createEventDispatcher();
    
    let formData = {
      name: service.name || '',
      description: service.description || '',
      duration_minutes: service.duration_minutes || 30,
      price: service.price || '',
      max_bookings_per_slot: service.max_bookings_per_slot || 1,
      buffer_time_minutes: service.buffer_time_minutes || 0,
      is_active: service.is_active !== false,
      business: businessId || service.business,
      
      // Advanced settings
      requires_deposit: service.requires_deposit || false,
      deposit_amount: service.deposit_amount || 0,
      cancellation_hours: service.cancellation_hours || 24,
      auto_confirm: service.auto_confirm !== false,
      
      // Availability
      available_days: service.available_days || [0, 1, 2, 3, 4, 5, 6],
      min_advance_hours: service.min_advance_hours || 0,
      max_advance_days: service.max_advance_days || 90
    };
    
    let errors = {};
    let showAdvancedSettings = false;
    
    const bufferOptions = [
      { value: 0, label: 'No buffer' },
      { value: 5, label: '5 minutes' },
      { value: 10, label: '10 minutes' },
      { value: 15, label: '15 minutes' },
      { value: 30, label: '30 minutes' },
      { value: 60, label: '1 hour' }
    ];
    
    const advanceBookingOptions = [
      { value: 0, label: 'Any time' },
      { value: 1, label: '1 hour' },
      { value: 2, label: '2 hours' },
      { value: 4, label: '4 hours' },
      { value: 12, label: '12 hours' },
      { value: 24, label: '24 hours' },
      { value: 48, label: '48 hours' }
    ];
    
    async function handleSubmit() {
      const validation = await validateForm(serviceSchema, formData);
      
      if (!validation.isValid) {
        errors = validation.errors;
        toast.error('Please check all required fields');
        return;
      }
      
      // Additional validations
      if (formData.requires_deposit && formData.deposit_amount <= 0) {
        errors.deposit_amount = 'Deposit amount must be greater than 0';
        return;
      }
      
      if (formData.requires_deposit && formData.deposit_amount >= formData.price) {
        errors.deposit_amount = 'Deposit must be less than service price';
        return;
      }
      
      errors = {};
      dispatch('submit', formData);
    }
    
    function handleCancel() {
      dispatch('cancel');
    }
    
    // Auto-calculate deposit amount as percentage
    $: if (formData.requires_deposit && !formData.deposit_amount && formData.price) {
      formData.deposit_amount = Math.round(formData.price * 0.2); // 20% default
    }
  </script>
  
  <form on:submit|preventDefault={handleSubmit} class="space-y-6">
    <Card title="Service Information">
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <div class="sm:col-span-2">
          <Input
            label="Service Name"
            bind:value={formData.name}
            error={errors.name}
            required
            placeholder="e.g., Haircut, Consultation, Deep Tissue Massage"
          />
        </div>
        
        <div class="sm:col-span-2">
          <label for="description" class="block text-sm font-medium text-gray-700 mb-1">
            Description
            <span class="text-red-500">*</span>
          </label>
          <textarea
            id="description"
            bind:value={formData.description}
            rows="4"
            class="
              block w-full rounded-md shadow-sm sm:text-sm
              {errors.description 
                ? 'border-red-300 text-red-900 focus:border-red-500 focus:ring-red-500' 
                : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'}
            "
            placeholder="Describe what this service includes, any preparations needed, etc."
          ></textarea>
          {#if errors.description}
            <p class="mt-1 text-sm text-red-600">{errors.description}</p>
          {/if}
          <p class="mt-1 text-xs text-gray-500">
            {formData.description.length}/500 characters
          </p>
        </div>
        
        <Select
          label="Duration"
          bind:value={formData.duration_minutes}
          options={DURATIONS}
          error={errors.duration_minutes}
          required
        />
        
        <Input
          label="Price"
          type="number"
          step="0.01"
          min="0"
          bind:value={formData.price}
          error={errors.price}
          required
          placeholder="0.00"
        />
        
        <Input
          label="Max Bookings per Time Slot"
          type="number"
          min="1"
          max="50"
          bind:value={formData.max_bookings_per_slot}
          placeholder="1"
        />
        
        <Select
          label="Buffer Time Between Bookings"
          bind:value={formData.buffer_time_minutes}
          options={bufferOptions}
        />
      </div>
      
      <div class="mt-6 space-y-4">
        <label class="flex items-center">
          <input
            type="checkbox"
            bind:checked={formData.is_active}
            class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <span class="ml-2 text-sm text-gray-700">Service is active and available for booking</span>
        </label>
        
        <label class="flex items-center">
          <input
            type="checkbox"
            bind:checked={formData.auto_confirm}
            class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
          />
          <span class="ml-2 text-sm text-gray-700">Auto-confirm bookings for this service</span>
        </label>
      </div>
    </Card>
    
    <!-- Advanced Settings -->
    <Card>
      <div slot="header" class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">Advanced Settings</h3>
        <button
          type="button"
          class="text-sm text-indigo-600 hover:text-indigo-500"
          on:click={() => showAdvancedSettings = !showAdvancedSettings}
        >
          {showAdvancedSettings ? 'Hide' : 'Show'}
        </button>
      </div>
      
      {#if showAdvancedSettings}
        <div class="space-y-6">
          <!-- Deposit Settings -->
          <div>
            <label class="flex items-center mb-3">
              <input
                type="checkbox"
                bind:checked={formData.requires_deposit}
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <span class="ml-2 text-sm font-medium text-gray-700">Require deposit for booking</span>
            </label>
            
            {#if formData.requires_deposit}
              <div class="ml-6 grid grid-cols-2 gap-4">
                <Input
                  label="Deposit Amount"
                  type="number"
                  step="0.01"
                  min="0"
                  bind:value={formData.deposit_amount}
                  error={errors.deposit_amount}
                  placeholder="0.00"
                />
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Percentage of Price
                  </label>
                  <p class="text-sm text-gray-500 mt-2">
                    {formData.price && formData.deposit_amount 
                      ? Math.round((formData.deposit_amount / formData.price) * 100) 
                      : 0}% of service price
                  </p>
                </div>
              </div>
            {/if}
          </div>
          
          <!-- Cancellation Policy -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Cancellation Policy
            </label>
            <Select
              bind:value={formData.cancellation_hours}
              options={[
                { value: 0, label: 'No restrictions' },
                { value: 1, label: '1 hour before' },
                { value: 2, label: '2 hours before' },
                { value: 4, label: '4 hours before' },
                { value: 12, label: '12 hours before' },
                { value: 24, label: '24 hours before' },
                { value: 48, label: '48 hours before' },
                { value: 72, label: '72 hours before' }
              ]}
            />
            <p class="mt-1 text-xs text-gray-500">
              Customers can cancel free of charge up to this time before the appointment
            </p>
          </div>
          
          <!-- Booking Advance Time -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Minimum Advance Booking
              </label>
              <Select
                bind:value={formData.min_advance_hours}
                options={advanceBookingOptions}
              />
              <p class="mt-1 text-xs text-gray-500">
                How far in advance bookings must be made
              </p>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Maximum Advance Booking
              </label>
              <Input
                type="number"
                min="1"
                max="365"
                bind:value={formData.max_advance_days}
                placeholder="90"
              />
              <p class="mt-1 text-xs text-gray-500">
                How many days ahead customers can book
              </p>
            </div>
          </div>
          
          <!-- Available Days -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Available Days
            </label>
            <div class="flex flex-wrap gap-3">
              {#each ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] as day, index}
                <label class="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.available_days.includes(index)}
                    on:change={(e) => {
                      if (e.target.checked) {
                        formData.available_days = [...formData.available_days, index];
                      } else {
                        formData.available_days = formData.available_days.filter(d => d !== index);
                      }
                    }}
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <span class="ml-2 text-sm text-gray-700">{day}</span>
                </label>
              {/each}
            </div>
          </div>
        </div>
      {/if}
    </Card>
    
    <div class="flex justify-end space-x-3">
      <Button variant="outline" type="button" on:click={handleCancel}>
        Cancel
      </Button>
      <Button type="submit" {loading}>
        {service.id ? 'Update' : 'Create'} Service
      </Button>
    </div>
  </form>