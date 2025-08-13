<!-- src/lib/components/business/BusinessHours.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
    import Select from '../common/Select.svelte';
    import Button from '../common/Button.svelte';
    import Card from '../common/Card.svelte';
    import Alert from '../common/Alert.svelte';
    import { WEEKDAYS, TIME_SLOTS } from '$lib/utils/constants';
    import toast from 'svelte-french-toast';
    
    export let hours = [];
    export let editable = false;
    export let loading = false;
    
    const dispatch = createEventDispatcher();
    
    // Initialize hours for all weekdays
    let businessHours = WEEKDAYS.map(day => {
      const existing = hours.find(h => h.weekday === day.value);
      return {
        weekday: day.value,
        weekday_display: day.label,
        opening_time: existing?.opening_time || '09:00',
        closing_time: existing?.closing_time || '17:00',
        is_closed: existing?.is_closed || false,
        break_start: existing?.break_start || null,
        break_end: existing?.break_end || null
      };
    });
    
    let hasUnsavedChanges = false;
    let showBreakTimes = false;
    
    function handleSave() {
      // Validate times
      for (const hour of businessHours) {
        if (!hour.is_closed) {
          if (hour.opening_time >= hour.closing_time) {
            toast.error(`Invalid hours for ${hour.weekday_display}: closing time must be after opening time`);
            return;
          }
          
          if (hour.break_start && hour.break_end) {
            if (hour.break_start >= hour.break_end) {
              toast.error(`Invalid break hours for ${hour.weekday_display}`);
              return;
            }
            if (hour.break_start <= hour.opening_time || hour.break_end >= hour.closing_time) {
              toast.error(`Break time must be within business hours for ${hour.weekday_display}`);
              return;
            }
          }
        }
      }
      
      dispatch('save', businessHours);
      hasUnsavedChanges = false;
    }
    
    function toggleDay(index) {
      businessHours[index].is_closed = !businessHours[index].is_closed;
      hasUnsavedChanges = true;
    }
    
    function copyToAll(index) {
      const source = businessHours[index];
      businessHours = businessHours.map((hour, i) => {
        if (i !== index) {
          return {
            ...hour,
            opening_time: source.opening_time,
            closing_time: source.closing_time,
            is_closed: source.is_closed,
            break_start: source.break_start,
            break_end: source.break_end
          };
        }
        return hour;
      });
      hasUnsavedChanges = true;
      toast.success('Hours copied to all days');
    }
    
    function copyWeekdays(index) {
      const source = businessHours[index];
      businessHours = businessHours.map((hour, i) => {
        if (i < 5 && i !== index) { // Monday to Friday
          return {
            ...hour,
            opening_time: source.opening_time,
            closing_time: source.closing_time,
            is_closed: source.is_closed,
            break_start: source.break_start,
            break_end: source.break_end
          };
        }
        return hour;
      });
      hasUnsavedChanges = true;
      toast.success('Hours copied to weekdays');
    }
    
    function setDefaultHours() {
      businessHours = businessHours.map((hour, i) => ({
        ...hour,
        opening_time: i < 5 ? '09:00' : '10:00', // Weekdays vs Weekend
        closing_time: i < 5 ? '17:00' : '16:00',
        is_closed: i === 6, // Closed on Sunday
        break_start: null,
        break_end: null
      }));
      hasUnsavedChanges = true;
    }
    
    function onChange() {
      hasUnsavedChanges = true;
    }
  </script>
  
  <Card>
    <div slot="header" class="flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900">Business Hours</h3>
      {#if editable}
        <div class="flex items-center gap-2">
          <Button variant="outline" size="sm" on:click={setDefaultHours}>
            Set Default
          </Button>
          <label class="flex items-center text-sm">
            <input
              type="checkbox"
              bind:checked={showBreakTimes}
              class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded mr-2"
            />
            Show break times
          </label>
        </div>
      {/if}
    </div>
    
    <div class="space-y-3">
      {#if hasUnsavedChanges}
        <Alert type="info">
          You have unsaved changes. Click "Save Hours" to apply them.
        </Alert>
      {/if}
      
      {#each businessHours as hour, index}
        <div class="flex items-center space-x-3 py-2 {hour.is_closed ? 'opacity-60' : ''}">
          <!-- Day Name -->
          <div class="w-28">
            <span class="text-sm font-medium text-gray-700">
              {hour.weekday_display}
            </span>
          </div>
          
          {#if editable}
            <!-- Open/Closed Toggle -->
            <label class="flex items-center">
              <input
                type="checkbox"
                checked={!hour.is_closed}
                on:change={() => toggleDay(index)}
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <span class="ml-2 text-sm text-gray-600">Open</span>
            </label>
            
            {#if !hour.is_closed}
              <!-- Opening Time -->
              <Select
                bind:value={hour.opening_time}
                options={TIME_SLOTS}
                on:change={onChange}
              />
              
              <span class="text-gray-500">to</span>
              
              <!-- Closing Time -->
              <Select
                bind:value={hour.closing_time}
                options={TIME_SLOTS}
                on:change={onChange}
              />
              
              {#if showBreakTimes}
                <span class="text-gray-500">Break:</span>
                
                <Select
                  bind:value={hour.break_start}
                  options={[{ value: null, label: 'None' }, ...TIME_SLOTS]}
                  on:change={onChange}
                />
                
                {#if hour.break_start}
                  <span class="text-gray-500">to</span>
                  
                  <Select
                    bind:value={hour.break_end}
                    options={TIME_SLOTS}
                    on:change={onChange}
                  />
                {/if}
              {/if}
              
              <!-- Copy Actions -->
              <div class="flex gap-1">
                <button
                  type="button"
                  class="text-xs text-indigo-600 hover:text-indigo-500"
                  on:click={() => copyToAll(index)}
                  title="Copy to all days"
                >
                  Copy all
                </button>
                {#if index < 5}
                  <button
                    type="button"
                    class="text-xs text-indigo-600 hover:text-indigo-500"
                    on:click={() => copyWeekdays(index)}
                    title="Copy to weekdays"
                  >
                    Weekdays
                  </button>
                {/if}
              </div>
            {:else}
              <span class="text-sm text-gray-500">Closed</span>
            {/if}
          {:else}
            <!-- Read-only view -->
            {#if hour.is_closed}
              <span class="text-sm text-gray-500">Closed</span>
            {:else}
              <span class="text-sm text-gray-900">
                {hour.opening_time} - {hour.closing_time}
              </span>
              {#if hour.break_start && hour.break_end}
                <span class="text-sm text-gray-500">
                  (Break: {hour.break_start} - {hour.break_end})
                </span>
              {/if}
            {/if}
          {/if}
        </div>
      {/each}
      
      {#if editable}
        <div class="pt-4 border-t border-gray-200 flex justify-end">
          <Button on:click={handleSave} {loading}>
            Save Hours
          </Button>
        </div>
      {/if}
    </div>
  </Card>