<!-- src/lib/components/common/Input.svelte -->
<script>
    export let type = 'text';
    export let label = '';
    export let value = '';
    export let placeholder = '';
    export let error = '';
    export let required = false;
    export let disabled = false;
    export let readonly = false;
    export let autocomplete = '';
    export let name = '';
    export let id = name || Math.random().toString(36).substr(2, 9);
    
    function handleInput(event) {
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
    
    <input
      {id}
      {type}
      {name}
      {placeholder}
      {disabled}
      {readonly}
      {required}
      {autocomplete}
      {value}
      on:input={handleInput}
      on:blur
      on:focus
      on:change
      class="
        block w-full rounded-md shadow-sm
        {error 
          ? 'border-red-300 text-red-900 placeholder-red-300 focus:border-red-500 focus:ring-red-500' 
          : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'}
        disabled:bg-gray-50 disabled:text-gray-500
        sm:text-sm
      "
    />
    
    {#if error}
      <p class="mt-1 text-sm text-red-600">{error}</p>
    {/if}
  </div>