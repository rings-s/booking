<!-- src/routes/businesses/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { businessAPI } from '$lib/api/businesses';
    import BusinessCard from '$lib/components/business/BusinessCard.svelte';
    import SearchBar from '$lib/components/search/SearchBar.svelte';
    import FilterPanel from '$lib/components/search/FilterPanel.svelte';
    import MapView from '$lib/components/common/MapView.svelte';
    import Pagination from '$lib/components/common/Pagination.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import toast from 'svelte-french-toast';
    
    let businesses = [];
    let loading = true;
    let searchQuery = '';
    let selectedCategory = '';
    let selectedLocation = '';
    let sortBy = 'relevance';
    let viewMode = 'grid'; // 'grid', 'list', 'map'
    let showFilters = false;
    let currentPage = 1;
    let totalPages = 1;
    let totalResults = 0;
    
    // Filter states
    let filters = {
      priceRange: '',
      rating: 0,
      openNow: false,
      hasOffers: false,
      categories: [],
      services: [],
      distance: 10
    };
    
    // Get query params
    $: searchQuery = $page.url.searchParams.get('q') || '';
    $: selectedCategory = $page.url.searchParams.get('category') || '';
    
    onMount(async () => {
      await searchBusinesses();
    });
    
    async function searchBusinesses() {
      loading = true;
      
      const params = {
        search: searchQuery,
        category: selectedCategory,
        location: selectedLocation,
        sort_by: sortBy,
        page: currentPage,
        ...filters
      };
      
      const { data, error } = await businessAPI.search(params);
      
      if (data) {
        businesses = data.results;
        totalPages = data.total_pages;
        totalResults = data.count;
      } else if (error) {
        toast.error('Failed to load businesses');
      }
      
      loading = false;
    }
    
    function handleSearch(event) {
      searchQuery = event.detail.query;
      selectedLocation = event.detail.location;
      currentPage = 1;
      updateURL();
      searchBusinesses();
    }
    
    function handleFilterChange() {
      currentPage = 1;
      searchBusinesses();
    }
    
    function updateURL() {
      const params = new URLSearchParams();
      if (searchQuery) params.set('q', searchQuery);
      if (selectedCategory) params.set('category', selectedCategory);
      if (selectedLocation) params.set('location', selectedLocation);
      
      goto(`/businesses?${params.toString()}`, { replaceState: true });
    }
    
    const sortOptions = [
      { value: 'relevance', label: 'Most Relevant' },
      { value: 'rating', label: 'Highest Rated' },
      { value: 'reviews', label: 'Most Reviewed' },
      { value: 'distance', label: 'Nearest First' },
      { value: 'price_low', label: 'Price: Low to High' },
      { value: 'price_high', label: 'Price: High to Low' }
    ];
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <!-- Search Header -->
    <div class="bg-gradient-to-r from-indigo-600 to-purple-600 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-white mb-6">Find Your Perfect Service</h1>
        <SearchBar 
          bind:query={searchQuery}
          bind:location={selectedLocation}
          on:search={handleSearch}
          class="max-w-3xl"
        />
        
        <!-- Quick Categories -->
        <div class="mt-6 flex flex-wrap gap-2">
          {#each ['Salon', 'Spa', 'Fitness', 'Healthcare', 'Education', 'Automotive'] as category}
            <button
              class="px-4 py-2 rounded-full text-sm font-medium transition-all
                     {selectedCategory === category 
                       ? 'bg-white text-indigo-600' 
                       : 'bg-white/20 text-white hover:bg-white/30'}"
              on:click={() => {
                selectedCategory = selectedCategory === category ? '' : category;
                handleFilterChange();
              }}
            >
              {category}
            </button>
          {/each}
        </div>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Toolbar -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-4">
          <Button
            variant="outline"
            size="sm"
            on:click={() => showFilters = !showFilters}
          >
            <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            Filters {#if Object.values(filters).some(v => v)}<span class="ml-1 px-2 py-0.5 text-xs bg-indigo-600 text-white rounded-full">Active</span>{/if}
          </Button>
          
          <select
            bind:value={sortBy}
            on:change={searchBusinesses}
            class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            {#each sortOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
          
          <span class="text-sm text-gray-600">
            {totalResults} businesses found
          </span>
        </div>
        
        <div class="flex items-center space-x-2">
          <!-- View Mode Toggles -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 flex">
            {#each [
              { mode: 'grid', icon: 'M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z' },
              { mode: 'list', icon: 'M4 6h16M4 12h16M4 18h16' },
              { mode: 'map', icon: 'M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7' }
            ] as view}
              <button
                class="p-2 {viewMode === view.mode ? 'bg-indigo-100 text-indigo-600' : 'text-gray-600 hover:bg-gray-100'}"
                on:click={() => viewMode = view.mode}
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d={view.icon} />
                </svg>
              </button>
            {/each}
          </div>
        </div>
      </div>
      
      <div class="flex gap-6">
        <!-- Filters Sidebar -->
        {#if showFilters}
          <div class="w-64 flex-shrink-0">
            <FilterPanel 
              bind:filters
              on:change={handleFilterChange}
            />
          </div>
        {/if}
        
        <!-- Results -->
        <div class="flex-1">
          {#if loading}
            <div class="flex justify-center py-12">
              <Spinner size="lg">Loading businesses...</Spinner>
            </div>
          {:else if businesses.length === 0}
            <div class="text-center py-12">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <h3 class="mt-2 text-lg font-medium text-gray-900">No businesses found</h3>
              <p class="mt-1 text-sm text-gray-500">Try adjusting your search or filters</p>
              <div class="mt-6">
                <Button variant="outline" on:click={() => {
                  searchQuery = '';
                  filters = {};
                  searchBusinesses();
                }}>
                  Clear Filters
                </Button>
              </div>
            </div>
          {:else if viewMode === 'map'}
            <MapView 
              {businesses}
              on:select={(e) => goto(`/businesses/${e.detail.slug}`)}
              class="h-[600px] rounded-lg shadow-lg"
            />
          {:else}
            <div class="{viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6' : 'space-y-4'}">
              {#each businesses as business}
                <BusinessCard 
                  {business}
                  view={viewMode}
                  on:click={() => goto(`/businesses/${business.slug}`)}
                />
              {/each}
            </div>
            
            <!-- Pagination -->
            {#if totalPages > 1}
              <div class="mt-8">
                <Pagination
                  bind:currentPage
                  {totalPages}
                  on:change={searchBusinesses}
                />
              </div>
            {/if}
          {/if}
        </div>
      </div>
    </div>
  </div>