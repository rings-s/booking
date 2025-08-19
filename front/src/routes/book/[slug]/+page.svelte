<!-- src/routes/book/[slug]/+page.svelte -->
<script>
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { authStore } from '$lib/stores/auth';
    import BookingForm from '$lib/components/booking/BookingForm.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Button from '$lib/components/common/Button.svelte';
    import Alert from '$lib/components/common/Alert.svelte';
    import { formatCurrency } from '$lib/utils/formatters';
    import toast from 'svelte-french-toast';

    export let data;
    const { business, services } = data;

    let showLoginPrompt = false;
    let selectedService = null;
    
    // Check if user is authenticated
    onMount(() => {
        if (!$authStore.isAuthenticated) {
            showLoginPrompt = true;
        }
    });

    function handleBookingSuccess(event) {
        const { booking } = event.detail;
        toast.success('Booking created successfully!');
        goto(`/bookings/${booking.id}`);
    }

    function handleBookingError(event) {
        const { error } = event.detail;
        toast.error(error || 'Failed to create booking');
    }

    function handleLoginRedirect() {
        const returnUrl = encodeURIComponent($page.url.pathname + $page.url.search);
        goto(`/auth/login?returnUrl=${returnUrl}`);
    }
</script>

<svelte:head>
    <title>Book Service - {business.name}</title>
    <meta name="description" content="Book a service at {business.name}. {business.description || ''}" />
</svelte:head>

<div class="min-h-screen bg-gray-50 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Business Header -->
        <div class="mb-8">
            <Card>
                <div class="flex items-start space-x-4">
                    {#if business.logo}
                        <img 
                            src={business.logo} 
                            alt="{business.name} logo"
                            class="w-16 h-16 rounded-lg object-cover flex-shrink-0"
                        />
                    {/if}
                    <div class="flex-1">
                        <h1 class="text-2xl font-bold text-gray-900 mb-2">
                            Book a Service at {business.name}
                        </h1>
                        {#if business.description}
                            <p class="text-gray-600 mb-3">{business.description}</p>
                        {/if}
                        <div class="flex items-center space-x-4 text-sm text-gray-500">
                            {#if business.location}
                                <div class="flex items-center">
                                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                        <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                                    </svg>
                                    {business.location}
                                </div>
                            {/if}
                            {#if business.phone}
                                <div class="flex items-center">
                                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                                    </svg>
                                    {business.phone}
                                </div>
                            {/if}
                        </div>
                    </div>
                </div>
            </Card>
        </div>

        <!-- Services Overview -->
        {#if services?.length > 0}
            <div class="mb-8">
                <Card>
                    <h2 class="text-lg font-semibold text-gray-900 mb-4">Available Services</h2>
                    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        {#each services as service}
                            <div class="border rounded-lg p-4 hover:shadow-md transition-shadow">
                                <h3 class="font-medium text-gray-900 mb-2">{service.name}</h3>
                                {#if service.description}
                                    <p class="text-sm text-gray-600 mb-3">{service.description}</p>
                                {/if}
                                <div class="flex items-center justify-between">
                                    <div class="text-sm text-gray-500">
                                        <div>{formatCurrency(service.price)}</div>
                                        <div>{service.duration} min</div>
                                    </div>
                                    <Button
                                        size="sm"
                                        variant={selectedService?.id === service.id ? 'primary' : 'outline'}
                                        on:click={() => selectedService = service}
                                    >
                                        {selectedService?.id === service.id ? 'Selected' : 'Select'}
                                    </Button>
                                </div>
                            </div>
                        {/each}
                    </div>
                </Card>
            </div>
        {/if}

        <!-- Login Prompt for Non-Authenticated Users -->
        {#if showLoginPrompt}
            <div class="mb-8">
                <Alert type="info">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="font-medium">Sign in to book a service</h3>
                            <p class="text-sm mt-1">You need to be logged in to make a booking.</p>
                        </div>
                        <Button on:click={handleLoginRedirect}>
                            Sign In
                        </Button>
                    </div>
                </Alert>
            </div>
        {:else}
            <!-- Booking Form -->
            <Card>
                <h2 class="text-xl font-bold text-gray-900 mb-6">Book Your Appointment</h2>
                <BookingForm 
                    {business} 
                    service={selectedService}
                    on:success={handleBookingSuccess}
                    on:error={handleBookingError}
                />
            </Card>
        {/if}

        <!-- Business Info -->
        <div class="mt-8">
            <Card>
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Business Information</h3>
                <div class="grid gap-6 md:grid-cols-2">
                    <!-- Contact Information -->
                    <div>
                        <h4 class="font-medium text-gray-900 mb-2">Contact</h4>
                        <div class="space-y-2 text-sm text-gray-600">
                            {#if business.email}
                                <div class="flex items-center">
                                    <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                                        <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                                    </svg>
                                    <a href="mailto:{business.email}" class="hover:text-blue-600">
                                        {business.email}
                                    </a>
                                </div>
                            {/if}
                            {#if business.phone}
                                <div class="flex items-center">
                                    <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z" />
                                    </svg>
                                    <a href="tel:{business.phone}" class="hover:text-blue-600">
                                        {business.phone}
                                    </a>
                                </div>
                            {/if}
                            {#if business.website}
                                <div class="flex items-center">
                                    <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                        <path fill-rule="evenodd" d="M4.083 9h1.946c.089-1.546.383-2.97.837-4.118A6.004 6.004 0 004.083 9zM10 2a8 8 0 100 16 8 8 0 000-16zm0 2c-.076 0-.232.032-.465.262-.238.234-.497.623-.737 1.182-.389.907-.673 2.142-.766 3.556h3.936c-.093-1.414-.377-2.649-.766-3.556-.24-.559-.5-.948-.737-1.182C10.232 4.032 10.076 4 10 4zm3.971 5c-.089-1.546-.383-2.97-.837-4.118A6.004 6.004 0 0115.917 9h-1.946zm-2.003 2H8.032c.093 1.414.377 2.649.766 3.556.24.559.5.948.737 1.182.233.23.389.262.465.262.076 0 .232-.032.465-.262.238-.234.498-.623.737-1.182.389-.907.673-2.142.766-3.556zm1.166 4.118c.454-1.147.748-2.572.837-4.118h1.946a6.004 6.004 0 01-2.783 4.118zm-6.268 0C6.412 13.97 6.118 12.546 6.03 11H4.083a6.004 6.004 0 002.783 4.118z" clip-rule="evenodd" />
                                    </svg>
                                    <a href={business.website} target="_blank" rel="noopener noreferrer" class="hover:text-blue-600">
                                        Visit Website
                                    </a>
                                </div>
                            {/if}
                        </div>
                    </div>

                    <!-- Business Hours -->
                    {#if business.hours && business.hours.length > 0}
                        <div>
                            <h4 class="font-medium text-gray-900 mb-2">Hours</h4>
                            <div class="space-y-1 text-sm text-gray-600">
                                {#each business.hours as hour}
                                    <div class="flex justify-between">
                                        <span class="capitalize">{hour.day_of_week}</span>
                                        <span>
                                            {#if hour.is_closed}
                                                Closed
                                            {:else}
                                                {hour.open_time} - {hour.close_time}
                                            {/if}
                                        </span>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    {/if}
                </div>
            </Card>
        </div>
    </div>
</div>