<script>
  import { createEventDispatcher, onMount } from 'svelte';

  // Props to match usage in +page.svelte
  export let query = '';
  export let location = '';
  export let placeholder = 'Search';
  export let locationPlaceholder = 'Location';
  export let autoFocus = false;
  export let disabled = false;
  export let name = 'search';

  const dispatch = createEventDispatcher();

  let queryEl;

  onMount(() => {
    if (autoFocus && queryEl) queryEl.focus();
  });

  function handleSubmit(e) {
    e.preventDefault();
    dispatch('search', { query, location });
  }

  function clear() {
    query = '';
    dispatch('input', { query, location });
    queryEl?.focus();
  }
</script>

<form class="relative w-full" {...$$restProps} role="search" on:submit|preventDefault={handleSubmit}>
  <label class="sr-only" for={name}>Search</label>

  <div class="flex flex-col gap-2 sm:flex-row sm:items-center">
    <div class="relative flex-1">
      <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="h-5 w-5">
          <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 1 0 3.473 9.75l3.638 3.639a.75.75 0 1 0 1.06-1.06l-3.64-3.639A5.5 5.5 0 0 0 9 3.5Zm-4 5.5a4 4 0 1 1 8.001 0A4 4 0 0 1 5 9Z" clip-rule="evenodd" />
        </svg>
      </span>
      <input
        bind:this={queryEl}
        id={name}
        name={name}
        class="block w-full rounded-lg border border-gray-300 bg-white pl-10 pr-10 py-2 text-sm placeholder-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/40 disabled:cursor-not-allowed disabled:opacity-60"
        type="search"
        {placeholder}
        {disabled}
        bind:value={query}
      />
      {#if query}
        <button type="button" class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400 hover:text-gray-600" on:click={clear} aria-label="Clear search">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="h-5 w-5">
            <path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm-1.78-10.53a.75.75 0 1 0-1.06 1.06L8.94 10l-1.78 1.47a.75.75 0 1 0 1.06 1.06L10 11.06l1.78 1.47a.75.75 0 1 0 1.06-1.06L11.06 10l1.78-1.47a.75.75 0 1 0-1.06-1.06L10 8.94 8.22 7.47Z" clip-rule="evenodd" />
          </svg>
        </button>
      {/if}
    </div>

    <div class="relative w-full sm:w-64">
      <span class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="h-5 w-5">
          <path d="M10 2a6 6 0 00-6 6c0 4.5 6 10 6 10s6-5.5 6-10a6 6 0 00-6-6zm0 8a2 2 0 110-4 2 2 0 010 4z" />
        </svg>
      </span>
      <input
        class="block w-full rounded-lg border border-gray-300 bg-white pl-10 pr-3 py-2 text-sm placeholder-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/40"
        type="text"
        placeholder={locationPlaceholder}
        bind:value={location}
      />
    </div>

    <button type="submit" class="btn-primary px-5 py-2">
      <span class="hidden sm:inline">Search</span>
      <span class="sm:hidden">Go</span>
    </button>
  </div>
</form>

<style>
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
</style>
