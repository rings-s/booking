<!-- src/routes/auth/login/+page.svelte -->
<script>
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { authAPI } from '$lib/api/auth';
  import { auth } from '$lib/stores/auth';
  import Input from '$lib/components/common/Input.svelte';
  import Button from '$lib/components/common/Button.svelte';
  import Alert from '$lib/components/common/Alert.svelte';
  import toast from 'svelte-french-toast';
  import { googleAuth } from '$lib/utils/google-auth';
  
  let email = '';
  let password = '';
  let loading = false;
  let googleLoading = false;
  let errors = {};
  let showPassword = false;
  let rememberMe = false;
  let googleError = null;
  
  const redirectTo = $page.url.searchParams.get('redirect') || '/dashboard';
  
  async function handleSubmit() {
    errors = {};
    
    if (!email) {
      errors.email = 'Email is required';
    }
    if (!password) {
      errors.password = 'Password is required';
    }
    
    if (Object.keys(errors).length > 0) return;
    
    loading = true;
    
    try {
      const { data, error } = await authAPI.login({ email, password, remember_me: rememberMe });
      
      if (data) {
        // Store the auth state
        auth.setUser(data.user);
        toast.success('Welcome back!');
        
        // Use setTimeout to ensure toast shows before redirect
        setTimeout(() => {
          goto(redirectTo);
        }, 100);
      } else {
        errors.general = error || 'Invalid email or password';
        toast.error(errors.general);
      }
    } catch (err) {
      console.error('Login error:', err);
      errors.general = 'An error occurred during login';
      toast.error(errors.general);
    }
    
    loading = false;
  }
  
  async function handleGoogleLogin() {
    googleLoading = true;
    googleError = null;
    errors.general = null; // Clear any general errors
    
    try {
      // Listen for popup messages
      const messageHandler = (event) => {
        if (event.origin !== window.location.origin) return;
        
        if (event.data.type === 'GOOGLE_AUTH_SUCCESS') {
          toast.success('Successfully signed in with Google!');
          setTimeout(() => {
            goto(redirectTo);
          }, 100);
        } else if (event.data.type === 'GOOGLE_AUTH_ERROR') {
          googleError = event.data.error;
          toast.error(googleError);
        }
        
        googleLoading = false;
        window.removeEventListener('message', messageHandler);
      };
      
      window.addEventListener('message', messageHandler);
      
      // Open Google OAuth popup
      const data = await googleAuth.login();
      
      if (data && data.success) {
        // Popup opened successfully, wait for message
        console.log('Google OAuth popup opened successfully');
      }
      
    } catch (error) {
      console.error('Google login error:', error);
      googleError = error.message || 'Google sign-in is currently unavailable. Please try again later.';
      toast.error(googleError);
      googleLoading = false;
    }
  }
</script>

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
        
        <h2 class="mt-6 text-3xl font-extrabold text-gray-900">
          Welcome back
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Don't have an account?
          <a href="/auth/register" class="font-medium text-indigo-600 hover:text-indigo-500 ml-1">
            Sign up for free
          </a>
        </p>
      </div>
      
      <!-- Error Alerts -->
      {#if errors.general}
        <Alert type="error" dismissible on:dismiss={() => errors.general = null}>
          {errors.general}
        </Alert>
      {/if}
      
      {#if googleError}
        <Alert type="warning" dismissible on:dismiss={() => googleError = null}>
          {googleError}
          <div class="mt-2 text-sm">
            You can still sign in using your email and password below.
          </div>
        </Alert>
      {/if}
      
      <!-- Form -->
      <form class="mt-8 space-y-6" on:submit|preventDefault={handleSubmit}>
        <div class="space-y-4">
          <Input
            type="email"
            label="Email address"
            bind:value={email}
            error={errors.email}
            placeholder="you@example.com"
            autocomplete="email"
            required
          />
          
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div class="mt-1 relative">
              <input
                id="password"
                type={showPassword ? 'text' : 'password'}
                bind:value={password}
                class="appearance-none block w-full px-3 py-2 border rounded-lg shadow-sm
                       focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm
                       {errors.password ? 'border-red-300' : 'border-gray-300'}"
                placeholder="••••••••"
                autocomplete="current-password"
                required
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
                on:click={() => showPassword = !showPassword}
              >
                <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  {#if showPassword}
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  {:else}
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  {/if}
                </svg>
              </button>
            </div>
            {#if errors.password}
              <p class="mt-1 text-sm text-red-600">{errors.password}</p>
            {/if}
          </div>
        </div>
        
        <div class="flex items-center justify-between">
          <label class="flex items-center">
            <input
              type="checkbox"
              bind:checked={rememberMe}
              class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <span class="ml-2 text-sm text-gray-900">Remember me</span>
          </label>
          
          <a href="/auth/forgot-password" class="text-sm text-indigo-600 hover:text-indigo-500">
            Forgot password?
          </a>
        </div>
        
        <div>
          <Button type="submit" fullWidth {loading}>
            Sign in
          </Button>
        </div>
        
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">Or continue with</span>
          </div>
        </div>
        
        <div class="">
          <Button
            type="button"
            variant="outline"
            fullWidth
            loading={googleLoading}
            disabled={googleLoading}
            on:click={handleGoogleLogin}
          >
            {#if !googleLoading}
              <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
            {/if}
            {googleLoading ? 'Connecting to Google...' : 'Continue with Google'}
          </Button>
        </div>
      </form>
    </div>
  </div>
  
  <!-- Right Panel - Image/Graphics -->
  <div class="hidden lg:block relative w-0 flex-1">
    <div class="absolute inset-0 bg-gradient-to-br from-indigo-600 to-purple-600">
      <div class="absolute inset-0 bg-black opacity-20"></div>
      <div class="absolute inset-0 flex items-center justify-center p-12">
        <div class="max-w-md text-white">
          <h3 class="text-4xl font-bold mb-6">Manage Your Business with Ease</h3>
          <p class="text-lg mb-8 text-indigo-100">
            Join thousands of businesses already using our platform to streamline their operations and grow their customer base.
          </p>
          
          <div class="space-y-4">
            {#each [
              'Automated scheduling and reminders',
              'Secure payment processing',
              'Customer relationship management',
              'Real-time analytics and insights'
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
      {#each Array(5) as _, i}
        <div 
          class="absolute rounded-full bg-white opacity-10"
          style="
            left: {Math.random() * 100}%;
            top: {Math.random() * 100}%;
            width: {Math.random() * 200 + 100}px;
            height: {Math.random() * 200 + 100}px;
            animation: float {Math.random() * 10 + 10}s ease-in-out infinite;
            animation-delay: {Math.random() * 5}s;
          "
        ></div>
      {/each}
    </div>
  </div>
</div>

<style>
  @keyframes float {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-20px) scale(1.1); }
  }
</style>