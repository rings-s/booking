<script>
  import { createEventDispatcher } from 'svelte';

  // Filters object is bound from parent
  export let filters = {
    priceRange: '',
    rating: 0,
    openNow: false,
    hasOffers: false,
    categories: [],
    services: [],
    distance: 10
  };

  const dispatch = createEventDispatcher();

  function changed() {
    dispatch('change', { filters });
  }
</script>

<div class="card">
  <div class="card-body space-y-4">
    <h3 class="heading-3">Filters</h3>

    <!-- Price Range -->
    <div class="form-field">
      <label class="form-label">Price Range</label>
      <select class="w-full rounded-md border border-gray-300 py-2 px-3 text-sm" bind:value={filters.priceRange} on:change={changed}>
        <option value="">Any</option>
        <option value="$">$</option>
        <option value="$$">$$</option>
        <option value="$$$">$$$</option>
        <option value="$$$$">$$$$</option>
      </select>
    </div>

    <!-- Rating -->
    <div class="form-field">
      <label class="form-label">Minimum Rating</label>
      <input type="range" min="0" max="5" step="1" bind:value={filters.rating} on:input={changed} class="w-full" />
      <p class="form-help">{filters.rating} stars & up</p>
    </div>

    <!-- Toggles -->
    <div class="space-y-2">
      <label class="flex items-center gap-2">
        <input type="checkbox" bind:checked={filters.openNow} on:change={changed} />
        <span>Open now</span>
      </label>
      <label class="flex items-center gap-2">
        <input type="checkbox" bind:checked={filters.hasOffers} on:change={changed} />
        <span>Has offers</span>
      </label>
    </div>

    <!-- Distance -->
    <div class="form-field">
      <label class="form-label">Distance (km)</label>
      <input type="number" min="1" max="100" bind:value={filters.distance} on:input={changed} class="w-full rounded-md border border-gray-300 py-2 px-3 text-sm" />
    </div>

    <div class="flex gap-2 pt-2">
      <button type="button" class="btn-ghost" on:click={() => { filters = { priceRange: '', rating: 0, openNow: false, hasOffers: false, categories: [], services: [], distance: 10 }; changed(); }}>Reset</button>
      <button type="button" class="btn-primary" on:click={changed}>Apply</button>
    </div>
  </div>
</div>
