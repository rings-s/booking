<!-- src/lib/components/booking/TimeSlotPicker.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
    import { formatTime } from '$lib/utils/formatters';
    
    export let slots = [];
    export let selectedSlot = null;
    export let loading = false;
    
    const dispatch = createEventDispatcher();
    
    function selectSlot(slot) {
      selectedSlot = slot;
      dispatch('select', slot);
    }
  </script>
  
  <div class="bg-white rounded-lg shadow p-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Available Times</h3>
    
    {#if loading}
      <div class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
      </div>
    {:else if slots.length > 0}
      <div class="grid grid-cols-3 sm:grid-cols-4 gap-3">
        {#each slots as slot}
          <button
            type="button"
            class="
              px-4 py-2 rounded-md text-sm font-medium
              {selectedSlot?.start_time === slot.start_time
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}
            "
            on:click={() => selectSlot(slot)}
          >
            {formatTime(slot.start_time)}
          </button>
        {/each}
      </div>
    {:else}
      <p class="text-center text-gray-500 py-8">
        No available time slots for the selected date
      </p>
    {/if}
  </div>