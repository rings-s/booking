<script>
  import { createEventDispatcher } from 'svelte';

  let {
    businesses = [],
    selectedId = null,
    className = '',
    ...restProps
  } = $props();

  const dispatch = createEventDispatcher();

  // Utility to normalize lat/lng roughly into a [0,1] range for pseudo-plotting
  // Fallback: center everything if coords missing
  function toXY(b) {
    const lat = b?.latitude ?? b?.lat ?? b?.coords?.lat;
    const lng = b?.longitude ?? b?.lng ?? b?.coords?.lng;
    if (typeof lat !== 'number' || typeof lng !== 'number') {
      return { x: 0.5, y: 0.5, hasCoords: false };
    }
    // Normalize assuming typical world bounds; this is a very rough approximation
    const x = (lng + 180) / 360; // 0..1
    const y = 1 - (lat + 90) / 180; // 0..1 (invert so north is up)
    return { x: Math.min(Math.max(x, 0), 1), y: Math.min(Math.max(y, 0), 1), hasCoords: true };
  }

  function select(business) {
    dispatch('select', business);
  }
</script>

<div class={`relative w-full bg-surface overflow-hidden ${className}`} style="min-height: 400px;">
  <!-- Faux map background -->
  <div class="absolute inset-0 bg-[linear-gradient(0deg,rgba(0,0,0,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,0,0,0.03)_1px,transparent_1px)] bg-[size:24px_24px]"></div>

  <!-- Markers -->
  {#if businesses && businesses.length}
    {#each businesses as b, i}
      {#key b.id ?? b.slug ?? i}
        {#await Promise.resolve(toXY(b)) then pos}
          <button
            type="button"
            class="absolute -translate-x-1/2 -translate-y-full"
            style={`left:${pos.x * 100}%; top:${pos.y * 100}%;`}
            on:click={() => select(b)}
            aria-label={`Select ${b?.name ?? 'business'}`}
            title={b?.name}
          >
            <span class="relative block">
              <span class={`block h-5 w-5 rounded-full border-2 ${selectedId === (b.id ?? b.slug) ? 'border-primary bg-primary/90' : 'border-white bg-primary/70'} shadow`}></span>
              <span class="absolute left-1/2 top-5 -translate-x-1/2 whitespace-nowrap rounded bg-black/70 px-2 py-0.5 text-xs text-white">
                {b?.name ?? 'Business'}
              </span>
            </span>
          </button>
        {/await}
      {/key}
    {/each}
  {:else}
    <div class="absolute inset-0 flex items-center justify-center">
      <div class="text-center text-gray-500">
        <p class="mb-2 font-medium">No businesses to display on the map</p>
        <p class="text-sm">Try adjusting your search or filters.</p>
      </div>
    </div>
  {/if}

  <!-- Legend -->
  <div class="absolute bottom-3 left-3 rounded bg-white/90 px-3 py-2 text-xs shadow">
    <div class="flex items-center gap-2">
      <span class="inline-block h-3 w-3 rounded-full bg-primary"></span>
      <span>Business</span>
    </div>
  </div>
</div>

<style>
  /* Ensure the tooltip doesn't overflow the container visually too much */
  button > span > span + span {
    pointer-events: none;
  }
</style>
