<!-- Example component showing how to use the i18n system -->
<script>
	import { t, formatDate, formatCurrency } from '$lib/stores/i18n.js';
	import { currentLocale, isRTLStore } from '$lib/stores/i18n.js';
	import LanguageSwitcher from '../common/LanguageSwitcher.svelte';
	
	let exampleDate = new Date();
	let exampleAmount = 99.99;
</script>

<div class="max-w-4xl mx-auto p-8 space-y-8">
	<h1 class="text-3xl font-bold text-gray-900 mb-6">
		{$t('common.language')} Translation Example
	</h1>
	
	<!-- Language Switcher Demo -->
	<div class="bg-white p-6 rounded-lg shadow-md">
		<h2 class="text-xl font-semibold mb-4">Language Switcher Variants</h2>
		
		<div class="space-y-4">
			<div>
				<h3 class="text-sm font-medium text-gray-700 mb-2">Dropdown (Default)</h3>
				<LanguageSwitcher variant="dropdown" />
			</div>
			
			<div>
				<h3 class="text-sm font-medium text-gray-700 mb-2">Buttons</h3>
				<LanguageSwitcher variant="buttons" />
			</div>
			
			<div>
				<h3 class="text-sm font-medium text-gray-700 mb-2">Select</h3>
				<LanguageSwitcher variant="select" className="w-48" />
			</div>
		</div>
	</div>
	
	<!-- Basic Translations -->
	<div class="bg-white p-6 rounded-lg shadow-md">
		<h2 class="text-xl font-semibold mb-4">Basic Translations</h2>
		
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
			<div>
				<h3 class="text-sm font-medium text-gray-700">Common Actions</h3>
				<ul class="mt-2 space-y-1 text-sm">
					<li>• {$t('common.save')}</li>
					<li>• {$t('common.edit')}</li>
					<li>• {$t('common.delete')}</li>
					<li>• {$t('common.search')}</li>
					<li>• {$t('common.cancel')}</li>
				</ul>
			</div>
			
			<div>
				<h3 class="text-sm font-medium text-gray-700">Navigation</h3>
				<ul class="mt-2 space-y-1 text-sm">
					<li>• {$t('navigation.dashboard')}</li>
					<li>• {$t('navigation.businesses')}</li>
					<li>• {$t('navigation.bookings')}</li>
					<li>• {$t('navigation.customers')}</li>
					<li>• {$t('navigation.services')}</li>
				</ul>
			</div>
		</div>
	</div>
	
	<!-- Authentication -->
	<div class="bg-white p-6 rounded-lg shadow-md">
		<h2 class="text-xl font-semibold mb-4">Authentication Form Example</h2>
		
		<form class="space-y-4 max-w-sm">
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-1">
					{$t('auth.email')}
				</label>
				<input 
					type="email" 
					class="w-full px-3 py-2 border border-gray-300 rounded-md"
					placeholder={$t('auth.email')}
				/>
			</div>
			
			<div>
				<label class="block text-sm font-medium text-gray-700 mb-1">
					{$t('auth.password')}
				</label>
				<input 
					type="password" 
					class="w-full px-3 py-2 border border-gray-300 rounded-md"
					placeholder={$t('auth.password')}
				/>
			</div>
			
			<div class="flex items-center">
				<input type="checkbox" id="remember" class="mr-2" />
				<label for="remember" class="text-sm text-gray-600">
					{$t('auth.rememberMe')}
				</label>
			</div>
			
			<button 
				type="submit" 
				class="w-full bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700"
			>
				{$t('auth.login')}
			</button>
			
			<p class="text-sm text-center text-gray-600">
				{$t('auth.dontHaveAccount')}
				<a href="/auth/register" class="text-indigo-600 hover:text-indigo-700">
					{$t('auth.register')}
				</a>
			</p>
		</form>
	</div>
	
	<!-- Formatting Examples -->
	<div class="bg-white p-6 rounded-lg shadow-md">
		<h2 class="text-xl font-semibold mb-4">Formatting Examples</h2>
		
		<div class="space-y-3">
			<div>
				<span class="text-sm font-medium text-gray-700">Date: </span>
				<span>{formatDate(exampleDate, 'long')}</span>
			</div>
			
			<div>
				<span class="text-sm font-medium text-gray-700">Short Date: </span>
				<span>{formatDate(exampleDate, 'short')}</span>
			</div>
			
			<div>
				<span class="text-sm font-medium text-gray-700">Currency: </span>
				<span>{formatCurrency(exampleAmount)}</span>
			</div>
			
			<div>
				<span class="text-sm font-medium text-gray-700">Time: </span>
				<span>{formatDate(exampleDate, 'time')}</span>
			</div>
		</div>
	</div>
	
	<!-- Business Context -->
	<div class="bg-white p-6 rounded-lg shadow-md">
		<h2 class="text-xl font-semibold mb-4">Business Context Example</h2>
		
		<div class="border rounded-lg p-4">
			<h3 class="font-semibold text-gray-900">{$t('business.title')} Example</h3>
			
			<div class="mt-3 space-y-2 text-sm">
				<div><strong>{$t('business.name')}:</strong> Salon Beauty Pro</div>
				<div><strong>{$t('business.description')}:</strong> Professional hair and beauty services</div>
				<div><strong>{$t('business.phone')}:</strong> +1 (555) 123-4567</div>
				<div><strong>{$t('business.email')}:</strong> info@salonbeautypro.com</div>
			</div>
			
			<div class="mt-4 flex gap-2">
				<button class="px-4 py-2 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700">
					{$t('business.bookNow')}
				</button>
				<button class="px-4 py-2 border border-gray-300 text-gray-700 rounded text-sm hover:bg-gray-50">
					{$t('business.viewBusiness')}
				</button>
			</div>
		</div>
	</div>
	
	<!-- Current Locale Info -->
	<div class="bg-gray-50 p-6 rounded-lg">
		<h2 class="text-xl font-semibold mb-4">Current Locale Information</h2>
		
		<div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
			<div>
				<strong>Current Locale:</strong> {$currentLocale}
			</div>
			<div>
				<strong>Text Direction:</strong> {$isRTLStore ? 'Right-to-Left (RTL)' : 'Left-to-Right (LTR)'}
			</div>
		</div>
	</div>
	
	<!-- Error and Success Messages -->
	<div class="bg-white p-6 rounded-lg shadow-md">
		<h2 class="text-xl font-semibold mb-4">Messages</h2>
		
		<div class="space-y-3">
			<div class="p-3 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
				{$t('error.networkError')}
			</div>
			
			<div class="p-3 bg-green-50 border border-green-200 rounded text-green-700 text-sm">
				{$t('success.saved')}
			</div>
			
			<div class="p-3 bg-yellow-50 border border-yellow-200 rounded text-yellow-700 text-sm">
				{$t('validation.required')}
			</div>
		</div>
	</div>
</div>