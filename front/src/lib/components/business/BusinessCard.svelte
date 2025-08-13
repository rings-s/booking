<!-- src/lib/components/business/BusinessCard.svelte -->
<script>
    import { createEventDispatcher } from 'svelte';
    import { formatCurrency } from '$lib/utils/formatters';
    import Card from '../common/Card.svelte';
    import StarRating from '../review/StarRating.svelte';
    import Button from '../common/Button.svelte';
    
    export let business;
    export let showActions = false;
    export let showQuickActions = false;
    
    const dispatch = createEventDispatcher();
    
    function handleEdit(event) {
      event.preventDefault();
      event.stopPropagation();
      dispatch('edit', business);
    }
    
    function handleDelete(event) {
      event.preventDefault();
      event.stopPropagation();
      dispatch('delete', business);
    }
    
    function handleClone(event) {
      event.preventDefault();
      event.stopPropagation();
      dispatch('clone', business);
    }
  </script>
  
  <Card hoverable={true} padding="none" class="group relative">
    <a href="/businesses/{business.slug}" class="block">
      {#if business.cover_image}
        <img
          src={business.cover_image}
          alt={business.name}
          class="w-full h-48 object-cover"
        />
      {:else}
        <div class="w-full h-48 bg-gradient-to-r from-indigo-500 to-purple-600"></div>
      {/if}
      
      <div class="p-6">
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900">{business.name}</h3>
            <p class="text-sm text-gray-500">{business.category}</p>
          </div>
          {#if business.logo}
            <img
              src={business.logo}
              alt="{business.name} logo"
              class="w-12 h-12 rounded-full object-cover ml-4"
            />
          {/if}
        </div>
        
        <div class="mt-2">
          <StarRating rating={business.average_rating} showCount={true} count={business.total_reviews} />
        </div>
        
        <p class="mt-3 text-sm text-gray-600 line-clamp-2">
          {business.description}
        </p>
        
        <div class="mt-4 flex items-center text-sm text-gray-500">
          <svg class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          {business.city}, {business.state}
        </div>
        
        {#if business.services?.length > 0}
          <div class="mt-4 pt-4 border-t border-gray-200">
            <p class="text-sm text-gray-500">
              Starting from {formatCurrency(Math.min(...business.services.map(s => s.price)))}
            </p>
          </div>
        {/if}
      </div>
    </a>
    
    {#if showActions}
      <div class="px-6 pb-4 flex gap-2">
        <a
          href="/businesses/{business.slug}/edit"
          class="flex-1 text-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Edit
        </a>
        <a
          href="/businesses/{business.slug}/analytics"
          class="flex-1 text-center px-3 py-2 bg-indigo-600 rounded-md text-sm font-medium text-white hover:bg-indigo-700"
        >
          Analytics
        </a>
      </div>
    {/if}
    
    {#if showQuickActions}
      <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
        <div class="flex space-x-1">
          <Button
            size="sm"
            variant="secondary"
            on:click={handleEdit}
            class="!p-2"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </Button>
          <Button
            size="sm"
            variant="secondary"
            on:click={handleClone}
            class="!p-2"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </Button>
          <Button
            size="sm"
            variant="danger"
            on:click={handleDelete}
            class="!p-2"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </Button>
        </div>
      </div>
    {/if}
  </Card>