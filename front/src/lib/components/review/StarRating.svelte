<!-- src/lib/components/review/StarRating.svelte -->
<script>
    export let rating = 0;
    export let maxRating = 5;
    export let interactive = false;
    export let size = 'md';
    export let showCount = false;
    export let count = 0;
    
    const sizes = {
      sm: 'w-4 h-4',
      md: 'w-5 h-5',
      lg: 'w-6 h-6'
    };
    
    function setRating(value) {
      if (interactive) {
        rating = value;
      }
    }
  </script>
  
  <div class="flex items-center">
    <div class="flex">
      {#each Array(maxRating) as _, i}
        <button
          type="button"
          class="{interactive ? 'cursor-pointer' : 'cursor-default'}"
          disabled={!interactive}
          on:click={() => setRating(i + 1)}
        >
          <svg
            class="{sizes[size]} {i < rating ? 'text-yellow-400' : 'text-gray-300'}"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.286 3.957a1 1 0 00.95.69h4.162c.969 0 1.371 1.24.588 1.81l-3.37 2.448a1 1 0 00-.364 1.118l1.287 3.957c.3.921-.755 1.688-1.54 1.118l-3.37-2.448a1 1 0 00-1.175 0l-3.37 2.448c-.784.57-1.838-.197-1.539-1.118l1.287-3.957a1 1 0 00-.364-1.118L2.05 9.384c-.783-.57-.38-1.81.588-1.81h4.162a1 1 0 00.95-.69l1.286-3.957z" />
          </svg>
        </button>
      {/each}
    </div>
    
    {#if showCount && count > 0}
      <span class="ml-2 text-sm text-gray-500">({count})</span>
    {/if}
  </div>