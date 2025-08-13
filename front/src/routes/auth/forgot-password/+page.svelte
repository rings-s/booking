<!-- src/routes/auth/forgot-password/+page.svelte -->
<script>
  import { goto } from '$app/navigation';
  import Input from '$lib/components/common/Input.svelte';
  import Button from '$lib/components/common/Button.svelte';
  import Alert from '$lib/components/common/Alert.svelte';
  import toast from 'svelte-french-toast';
  
  let email = '';
  let loading = false;
  let errors = {};
  let emailSent = false;
  
  async function handleSubmit() {
    errors = {};
    
    if (!email) {
      errors.email = 'Email is required';
      return;
    }
    
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = 'Please enter a valid email address';
      return;
    }
    
    loading = true;
    
    try {
      // Simulate API call for password reset
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      emailSent = true;
      toast.success('Password reset email sent!');
    } catch (error) {
      errors.general = 'Failed to send password reset email. Please try again.';
    }
    
    loading = false;
  }
</script>

<svelte:head>
  <title>Forgot Password - BookingPro</title>
</svelte:head>

<div class="min-h-screen flex">
  <!-- Left Panel - Form -->
  <div class="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo -->
      <div class="text-center">
        <a href="/" class="inline-flex items-center space-x-2">
          <div class="w-12 h-12 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <span class="text-2xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            BookingPro
          </span>
        </a>
      </div>

      {#if !emailSent}
        <!-- Reset Password Form -->
        <div>
          <h2 class="mt-6 text-3xl font-extrabold text-gray-900 text-center">
            Forgot your password?
          </h2>
          <p class="mt-2 text-sm text-gray-600 text-center">
            Enter your email address and we'll send you a link to reset your password.
          </p>
        </div>
        
        <!-- Error Alert -->
        {#if errors.general}
          <Alert type="error" dismissible on:dismiss={() => errors.general = null}>
            {errors.general}
          </Alert>
        {/if}
        
        <form class="mt-8 space-y-6" on:submit|preventDefault={handleSubmit}>
          <div>
            <Input
              type="email"
              label="Email address"
              bind:value={email}
              error={errors.email}
              placeholder="you@example.com"
              autocomplete="email"
              required
            />
          </div>
          
          <div>
            <Button type="submit" fullWidth {loading}>
              {loading ? 'Sending...' : 'Send reset link'}
            </Button>
          </div>
          
          <div class="text-center">
            <p class="text-sm text-gray-600">
              Remember your password?
              <a href="/auth/login" class="font-medium text-indigo-600 hover:text-indigo-500 ml-1">
                Sign in
              </a>
            </p>
          </div>
        </form>
      {:else}
        <!-- Success Message -->
        <div class="text-center">
          <div class="w-16 h-16 mx-auto mb-6 bg-green-100 rounded-full flex items-center justify-center">
            <svg class="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </div>
          
          <h2 class="text-3xl font-extrabold text-gray-900 mb-4">
            Check your email
          </h2>
          
          <p class="text-gray-600 mb-8">
            We've sent a password reset link to <span class="font-semibold">{email}</span>
          </p>
          
          <div class="space-y-4">
            <Button fullWidth on:click={() => goto('/auth/login')}>
              Back to login
            </Button>
            
            <button
              type="button"
              class="text-sm text-indigo-600 hover:text-indigo-500"
              on:click={() => emailSent = false}
            >
              Didn't receive the email? Try again
            </button>
          </div>
        </div>
      {/if}
    </div>
  </div>
  
  <!-- Right Panel - Image/Graphics -->
  <div class="hidden lg:block relative w-0 flex-1">
    <div class="absolute inset-0 bg-gradient-to-br from-purple-600 to-indigo-600">
      <div class="absolute inset-0 bg-black opacity-20"></div>
      <div class="absolute inset-0 flex items-center justify-center p-12">
        <div class="max-w-md text-white">
          <h3 class="text-4xl font-bold mb-6">Don't worry, we've got you covered</h3>
          <p class="text-lg mb-8 text-purple-100">
            Password resets happen to the best of us. We'll get you back into your account in no time.
          </p>
          
          <div class="space-y-4">
            {#each [
              'Secure password reset process',
              'Email verification for security',
              'Quick and easy recovery',
              '24/7 customer support available'
            ] as feature}
              <div class="flex items-center">
                <svg class="w-6 h-6 mr-3 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span>{feature}</span>
              </div>
            {/each}
          </div>
        </div>
      </div>
      
      <!-- Decorative Elements -->
      {#each Array(4) as _, i}
        <div 
          class="absolute rounded-full bg-white opacity-10"
          style="
            left: {Math.random() * 100}%;
            top: {Math.random() * 100}%;
            width: {Math.random() * 150 + 75}px;
            height: {Math.random() * 150 + 75}px;
            animation: float {Math.random() * 8 + 12}s ease-in-out infinite;
            animation-delay: {Math.random() * 4}s;
          "
        ></div>
      {/each}
    </div>
  </div>
</div>

<style>
  @keyframes float {
    0%, 100% { 
      transform: translateY(0) scale(1) rotate(0deg); 
      opacity: 0.1;
    }
    50% { 
      transform: translateY(-30px) scale(1.05) rotate(5deg); 
      opacity: 0.15;
    }
  }
</style>