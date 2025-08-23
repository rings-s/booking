<!-- src/lib/components/common/Select.svelte -->
<script>
    let {
        label = '',
        value = $bindable(''),
        options = [],
        placeholder = 'Select an option',
        error = '',
        required = false,
        disabled = false,
        name = '',
        id = name || Math.random().toString(36).substr(2, 9),
        ...restProps
    } = $props();
    
    function handleChange(event) {
      value = event.target.value;
    }
  </script>
  
  <div class="mb-4">
    {#if label}
      <label for={id} class="block text-sm font-medium text-gray-700 mb-1">
        {label}
        {#if required}
          <span class="text-red-500">*</span>
        {/if}
      </label>
    {/if}
    
    <select
      {id}
      {name}
      {disabled}
      {required}
      bind:value
      onchange={handleChange}
      {...restProps}
      class="
        block w-full rounded-md shadow-sm
        {error 
          ? 'border-red-300 text-red-900 focus:border-red-500 focus:ring-red-500' 
          : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'}
        disabled:bg-gray-50 disabled:text-gray-500
        sm:text-sm
      "
    >
      <option value="" disabled selected={!value}>
        {placeholder}
      </option>
      {#each options as option}
        <option value={option.value || option}>
          {option.label || option}
        </option>
      {/each}
    </select>
    
    {#if error}
      <p class="mt-1 text-sm text-red-600">{error}</p>
    {/if}
  </div>