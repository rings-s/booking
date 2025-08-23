<!-- src/lib/components/common/Pagination.svelte -->
<script>
  import Button from './Button.svelte';

  // Public props
  let {
    page = 1,               // 1-indexed
    totalPages = undefined, // optional when using totalItems + perPage
    totalItems = undefined, // optional
    perPage = undefined,    // optional
    siblingCount = 1,       // pages around the current
    boundaryCount = 1,      // pages at the edges
    compact = false,        // force compact layout
    showSummary = true,     // show "Page x of y"
    onchange = () => {},    // callback for page changes
    ...restProps
  } = $props();

  // Derived values
  let pagesCount = $derived(totalPages ?? (totalItems && perPage ? Math.max(1, Math.ceil(totalItems / perPage)) : 1));
  let current = $derived(clamp(page, 1, pagesCount));

  function clamp(n, min, max) { return Math.min(Math.max(n, min), max); }
  function range(start, end) { return start > end ? [] : Array.from({ length: end - start + 1 }, (_, i) => start + i); }

  function setPage(p) {
    const next = clamp(p, 1, pagesCount);
    if (next !== current) onchange({ page: next });
  }

  const ELLIPSIS = '…';
  let items = $derived(buildPagination(current, pagesCount, siblingCount, boundaryCount));

  function buildPagination(current, total, siblings = 1, boundaries = 1) {
    if (!total || total <= 1) return [1];

    const firstPages = range(1, Math.min(boundaries, total));
    const lastPages = range(Math.max(total - boundaries + 1, boundaries + 1), total);

    const start = Math.max(
      Math.min(current - siblings, total - boundaries - siblings * 2 - 1),
      boundaries + 2
    );

    const end = Math.min(
      Math.max(current + siblings, boundaries + siblings * 2 + 2),
      lastPages.length ? lastPages[0] - 2 : total - 1
    );

    const middle = start <= end ? range(start, end) : [];

    const withLeftEllipsis = start > boundaries + 2;
    const withRightEllipsis = end < (lastPages.length ? lastPages[0] - 2 : total - 1);

    return [
      ...firstPages,
      withLeftEllipsis ? ELLIPSIS : (boundaries + 1 <= total - boundaries ? boundaries + 1 : null),
      ...middle,
      withRightEllipsis ? ELLIPSIS : (total - boundaries >= boundaries + 1 ? total - boundaries : null),
      ...lastPages
    ].filter(Boolean);
  }
</script>

<!-- Container -->
<nav class="w-full flex items-center justify-between gap-3" aria-label="Pagination">
  <!-- Summary (left) -->
  {#if showSummary}
    <div class="text-sm text-gray-600 hidden sm:block">
      Page <span class="font-semibold text-gray-900">{current}</span>
      of <span class="font-semibold text-gray-900">{pagesCount}</span>
    </div>
  {/if}

  <!-- Desktop / Regular -->
  <div class="flex-1 hidden md:flex items-center justify-center">
    <div class="inline-flex items-center gap-1">
      <!-- Prev -->
      <Button size="md" variant="outline" disabled={current === 1} onclick={() => setPage(current - 1)} aria-label="Previous page">
        <svg class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        Prev
      </Button>

      <!-- Numbers -->
      {#each items as it}
        {#if it === ELLIPSIS}
          <span class="px-2 text-gray-400 select-none">{ELLIPSIS}</span>
        {:else}
          <button
            class="inline-flex items-center justify-center rounded-md border px-3 py-2 text-sm font-medium transition-colors
                   focus:outline-none focus:ring-2 focus:ring-offset-2
                   {it === current
                      ? 'bg-[var(--primary)] text-white border-[var(--primary-dark)] focus:ring-[var(--primary)]'
                      : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50 focus:ring-gray-300'}"
            aria-current={it === current ? 'page' : undefined}
            aria-label={`Page ${it}`}
            onclick={() => setPage(it)}
          >
            {it}
          </button>
        {/if}
      {/each}

      <!-- Next -->
      <Button size="md" variant="outline" disabled={current === pagesCount} onclick={() => setPage(current + 1)} aria-label="Next page">
        Next
        <svg class="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      </Button>
    </div>
  </div>

  <!-- Compact / Mobile -->
  {#if compact}
    <div class="flex-1 flex items-center justify-end gap-2">
      <Button size="md" variant="outline" disabled={current === 1} onclick={() => setPage(current - 1)} aria-label="Previous page">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      </Button>
      <div class="text-sm text-gray-700">
        <span class="font-semibold">{current}</span>
        <span class="text-gray-400">/</span>
        <span class="font-semibold">{pagesCount}</span>
      </div>
      <Button size="md" variant="outline" disabled={current === pagesCount} onclick={() => setPage(current + 1)} aria-label="Next page">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      </Button>
    </div>
  {:else}
    <div class="flex-1 flex items-center justify-end sm:justify-between gap-2 md:hidden">
      <Button size="md" variant="outline" disabled={current === 1} onclick={() => setPage(current - 1)} aria-label="Previous page">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
      </Button>
      <div class="text-sm text-gray-700">
        <span class="font-semibold">{current}</span>
        <span class="text-gray-400">/</span>
        <span class="font-semibold">{pagesCount}</span>
      </div>
      <Button size="md" variant="outline" disabled={current === pagesCount} onclick={() => setPage(current + 1)} aria-label="Next page">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      </Button>
    </div>
  {/if}
</nav>

<style>
  :global(.pagination-primary) {
    /* Helper class in case parent wants to enforce primary accent via CSS vars */
    --tw-ring-color: var(--primary);
  }
</style>
