<script>
	import { onMount } from 'svelte';
	import { availableLocales, currentLocale, changeLocale, isLoadingLocale } from '$lib/stores/i18n.js';
	import { t } from '$lib/stores/i18n.js';
	import Button from './Button.svelte';
	
	let { variant = 'dropdown', showFlags = true, className = '' } = $props();
	
	let isOpen = $state(false);
	let dropdownRef = $state();
	
	// Handle clicks outside dropdown to close it
	function handleClickOutside(event) {
		if (dropdownRef && !dropdownRef.contains(event.target)) {
			isOpen = false;
		}
	}
	
	onMount(() => {
		document.addEventListener('click', handleClickOutside);
		return () => {
			document.removeEventListener('click', handleClickOutside);
		};
	});
	
	async function handleLocaleChange(localeCode) {
		if ($currentLocale !== localeCode) {
			await changeLocale(localeCode);
			isOpen = false;
		}
	}
	
	// Find current locale info
	const currentLocaleInfo = $derived($availableLocales.find(locale => locale.code === $currentLocale) || $availableLocales[0]);
</script>

{#if variant === 'dropdown'}
	<div class="relative inline-block text-left {className}" bind:this={dropdownRef}>
		<button
			type="button"
			class="inline-flex items-center justify-center w-full px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
			disabled={$isLoadingLocale}
			onclick={() => isOpen = !isOpen}
			aria-haspopup="true"
			aria-expanded={isOpen}
		>
			{#if showFlags}
				<span class="mr-2" aria-hidden="true">{currentLocaleInfo.flag}</span>
			{/if}
			<span class="hidden sm:inline">{currentLocaleInfo.name}</span>
			<span class="sm:hidden">{currentLocaleInfo.code.toUpperCase()}</span>
			{#if $isLoadingLocale}
				<svg class="w-4 h-4 ml-2 animate-spin" fill="none" viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
				</svg>
			{:else}
				<svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
				</svg>
			{/if}
		</button>
		
		{#if isOpen}
			<div class="absolute right-0 z-50 w-48 mt-2 origin-top-right bg-white border border-gray-200 divide-y divide-gray-100 rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
				<div class="py-1">
					{#each $availableLocales as locale (locale.code)}
						<button
							type="button"
							class="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 {locale.code === $currentLocale ? 'bg-blue-50 text-blue-700' : ''}"
							onclick={() => handleLocaleChange(locale.code)}
							disabled={$isLoadingLocale}
						>
							{#if showFlags}
								<span class="mr-3" aria-hidden="true">{locale.flag}</span>
							{/if}
							<span>{locale.name}</span>
							{#if locale.code === $currentLocale}
								<svg class="w-4 h-4 ml-auto text-blue-600" fill="currentColor" viewBox="0 0 20 20">
									<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
								</svg>
							{/if}
						</button>
					{/each}
				</div>
			</div>
		{/if}
	</div>

{:else if variant === 'buttons'}
	<div class="flex flex-wrap gap-2 {className}">
		{#each $availableLocales as locale (locale.code)}
			<Button
				variant={locale.code === $currentLocale ? 'primary' : 'secondary'}
				size="sm"
				disabled={$isLoadingLocale}
				onclick={() => handleLocaleChange(locale.code)}
				class="flex items-center"
			>
				{#if showFlags}
					<span class="mr-1" aria-hidden="true">{locale.flag}</span>
				{/if}
				<span class="hidden sm:inline">{locale.name}</span>
				<span class="sm:hidden">{locale.code.toUpperCase()}</span>
			</Button>
		{/each}
	</div>

{:else if variant === 'select'}
	<div class="relative {className}">
		<label for="language-select" class="sr-only">{$t('common.language')}</label>
		<select
			id="language-select"
			class="block w-full px-3 py-2 text-sm border border-gray-300 rounded-md shadow-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
			value={$currentLocale}
			disabled={$isLoadingLocale}
			onchange={(e) => handleLocaleChange(e.target.value)}
		>
			{#each $availableLocales as locale (locale.code)}
				<option value={locale.code}>
					{showFlags ? `${locale.flag} ` : ''}{locale.name}
				</option>
			{/each}
		</select>
		{#if $isLoadingLocale}
			<div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
				<svg class="w-4 h-4 animate-spin text-gray-400" fill="none" viewBox="0 0 24 24">
					<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
					<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
				</svg>
			</div>
		{/if}
	</div>
{/if}