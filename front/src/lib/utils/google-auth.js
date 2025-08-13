// src/lib/utils/google-auth.js
import { PUBLIC_GOOGLE_CLIENT_ID } from '$env/static/public';
import { authAPI } from '$lib/api/auth';
import { auth } from '$lib/stores/auth';
import toast from 'svelte-french-toast';
import { browser } from '$app/environment';

class GoogleAuth {
  constructor() {
    this.clientId = PUBLIC_GOOGLE_CLIENT_ID;
    this.isInitialized = false;
    this._pendingPromise = null;
    this._initializationPromise = null;
    this._retryCount = 0;
    this._maxRetries = 3;
    
    // Set up message listener for popup communication
    if (browser) {
      this._setupMessageListener();
    }
  }

  // Load and initialize Google Identity Services with retry logic
  async initialize() {
    if (this.isInitialized) return;
    
    if (this._initializationPromise) {
      return this._initializationPromise;
    }
    
    this._initializationPromise = this._performInitialization();
    return this._initializationPromise;
  }
  
  async _performInitialization() {
    if (!browser) {
      throw new Error('Google Auth can only be initialized in browser environment');
    }
    
    if (!this.clientId) {
      const error = new Error('Google Client ID is not configured. Please check your environment variables.');
      toast.error('Google authentication is not properly configured');
      throw error;
    }

    try {
      // Load Google Identity Services script with retry
      await this._loadGoogleScriptWithRetry();
      
      // Initialize Google Auth for credential flow
      if (window.google?.accounts?.id) {
        window.google.accounts.id.initialize({
          client_id: this.clientId,
          callback: this.handleCredentialResponse.bind(this),
          auto_select: false,
          cancel_on_tap_outside: true,
          // Enable FedCM for future compatibility
          use_fedcm_for_prompt: true,
          ux_mode: 'popup'
        });
        
        this.isInitialized = true;
        console.info('Google Auth initialized successfully');
      } else {
        throw new Error('Google Identity Services not available after loading');
      }
    } catch (error) {
      console.error('Failed to initialize Google Auth:', error);
      toast.error('Failed to initialize Google authentication');
      this._initializationPromise = null; // Allow retry
      throw error;
    }
  }

  // Handle credential response from Google with enhanced error handling
  async handleCredentialResponse(response) {
    try {
      if (!response || !response.credential) {
        throw new Error('No credential received from Google');
      }
      
      // Show loading state
      const loadingToast = toast.loading('Authenticating with Google...');
      
      try {
        // Login via our backend with the JWT token
        const { data, error } = await authAPI.googleLogin(response.credential);
        
        toast.dismiss(loadingToast);
        
        if (error) {
          // Handle different types of errors
          if (typeof error === 'object') {
            const errorMessage = error.detail || error.message || 'Google authentication failed';
            throw new Error(errorMessage);
          }
          throw new Error(error);
        }

        if (!data || !data.user) {
          throw new Error('Invalid response from authentication server');
        }

        // Update auth store
        auth.setUser(data.user);
        toast.success(`Welcome ${data.user.first_name || 'back'}! Successfully signed in.`);
        
        // Resolve pending promise if it exists
        if (this._pendingPromise) {
          this._pendingPromise.resolve(data);
          this._pendingPromise = null;
        }
        
        return data;
      } catch (apiError) {
        toast.dismiss(loadingToast);
        throw apiError;
      }
      
    } catch (error) {
      console.error('Google credential error:', error);
      
      // Show appropriate error message
      let errorMessage = 'Google login failed';
      if (error.message) {
        if (error.message.includes('network')) {
          errorMessage = 'Network error. Please check your connection and try again.';
        } else if (error.message.includes('token')) {
          errorMessage = 'Authentication token error. Please try signing in again.';
        } else {
          errorMessage = error.message;
        }
      }
      
      toast.error(errorMessage);
      
      // Reject pending promise if it exists
      if (this._pendingPromise) {
        this._pendingPromise.reject(error);
        this._pendingPromise = null;
      }
      
      throw error;
    }
  }

  // Enhanced login method with multiple strategies
  async login() {
    try {
      // Ensure Google Auth is initialized
      await this.initialize();
      
      // Try direct credential flow first (faster)
      if (window.google?.accounts?.id) {
        return this._tryDirectLogin();
      } else {
        // Fallback to popup flow
        return this._tryPopupLogin();
      }
    } catch (error) {
      console.error('Google login error:', error);
      toast.error(error.message || 'Google login failed');
      throw error;
    }
  }
  
  // Try direct Google One Tap login
  async _tryDirectLogin() {
    return new Promise((resolve, reject) => {
      this._pendingPromise = { resolve, reject };
      
      try {
        // Show Google One Tap prompt
        window.google.accounts.id.prompt((notification) => {
          if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
            console.info('Google One Tap not shown, falling back to popup');
            this._tryPopupLogin().then(resolve).catch(reject);
          } else if (notification.isDismissedMoment()) {
            const error = new Error('Google sign-in was dismissed');
            reject(error);
          }
        });
        
        // Timeout after 10 seconds
        setTimeout(() => {
          if (this._pendingPromise) {
            console.info('Google One Tap timeout, falling back to popup');
            this._tryPopupLogin().then(resolve).catch(reject);
          }
        }, 10000);
        
      } catch (error) {
        console.warn('Direct login failed, trying popup:', error);
        this._tryPopupLogin().then(resolve).catch(reject);
      }
    });
  }
  
  // Try popup-based login
  async _tryPopupLogin() {
    return new Promise((resolve, reject) => {
      this._pendingPromise = { resolve, reject };
      
      try {
        // Open Google OAuth popup
        const authUrl = this.getAuthUrl();
        const popupFeatures = [
          'width=500',
          'height=600',
          'scrollbars=yes',
          'resizable=yes',
          'toolbar=no',
          'menubar=no',
          'location=no',
          'directories=no',
          'status=no',
          'copyhistory=no'
        ].join(',');
        
        const popup = window.open(authUrl, 'google-oauth', popupFeatures);
        
        if (!popup) {
          const error = new Error('Popup blocked. Please allow popups for this site and try again.');
          toast.error('Please allow popups and try again');
          reject(error);
          return;
        }
        
        // Center the popup
        const left = window.screenX + (window.outerWidth - 500) / 2;
        const top = window.screenY + (window.outerHeight - 600) / 2;
        popup.moveTo(left, top);
        
        // Focus the popup
        popup.focus();
        
        // Set up cleanup timeout
        const timeout = setTimeout(() => {
          if (this._pendingPromise) {
            reject(new Error('Authentication timed out. Please try again.'));
            this._pendingPromise = null;
          }
        }, 120000); // 2 minutes timeout
        
        // Store timeout ID for cleanup
        this._currentTimeout = timeout;
        
        // Return immediately - popup will communicate via postMessage
        return { success: true, popup };
        
      } catch (error) {
        console.error('Popup login error:', error);
        reject(error);
      }
    });
  }
  
  // Generate Google OAuth URL for popup with security enhancements
  getAuthUrl() {
    // Generate random state for CSRF protection
    const state = this._generateRandomState();
    
    const params = new URLSearchParams({
      client_id: this.clientId,
      redirect_uri: `${window.location.origin}/auth/google/callback`,
      response_type: 'code',
      scope: 'openid profile email',
      access_type: 'online',
      prompt: 'select_account',
      state: state,
      include_granted_scopes: 'true'
    });

    // Store state for validation
    if (browser) {
      sessionStorage.setItem('google_oauth_state', state);
    }

    return `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
  }
  
  // Generate random state for CSRF protection
  _generateRandomState() {
    const array = new Uint32Array(2);
    crypto.getRandomValues(array);
    return array.join('');
  }
  
  // Validate OAuth state parameter
  _validateState(receivedState) {
    if (!browser) return false;
    
    const storedState = sessionStorage.getItem('google_oauth_state');
    sessionStorage.removeItem('google_oauth_state'); // Clean up
    
    return storedState === receivedState;
  }
  
  // Cleanup method
  cleanup() {
    if (this._currentTimeout) {
      clearTimeout(this._currentTimeout);
      this._currentTimeout = null;
    }
    
    if (this._pendingPromise) {
      this._pendingPromise.reject(new Error('Authentication cancelled'));
      this._pendingPromise = null;
    }
    
    if (browser) {
      sessionStorage.removeItem('google_oauth_state');
    }
  }


  // Setup message listener for popup communication
  _setupMessageListener() {
    window.addEventListener('message', (event) => {
      // Verify origin for security
      if (event.origin !== window.location.origin) {
        return;
      }
      
      if (event.data.type === 'GOOGLE_AUTH_SUCCESS') {
        this._handlePopupSuccess(event.data.data);
      } else if (event.data.type === 'GOOGLE_AUTH_ERROR') {
        this._handlePopupError(event.data.error);
      }
    }, false);
  }
  
  // Handle popup success with cleanup
  _handlePopupSuccess(data) {
    try {
      // Clear timeout
      if (this._currentTimeout) {
        clearTimeout(this._currentTimeout);
        this._currentTimeout = null;
      }
      
      auth.setUser(data.user);
      toast.success(`Welcome ${data.user.first_name || 'back'}! Successfully signed in.`);
      
      if (this._pendingPromise) {
        this._pendingPromise.resolve(data);
        this._pendingPromise = null;
      }
    } catch (error) {
      console.error('Error handling popup success:', error);
      this._handlePopupError('Failed to process authentication result');
    }
  }
  
  // Handle popup error with cleanup
  _handlePopupError(error) {
    try {
      // Clear timeout
      if (this._currentTimeout) {
        clearTimeout(this._currentTimeout);
        this._currentTimeout = null;
      }
      
      console.error('Popup authentication error:', error);
      
      let errorMessage = 'Google authentication failed';
      if (typeof error === 'string') {
        errorMessage = error;
      } else if (error && error.message) {
        errorMessage = error.message;
      }
      
      toast.error(errorMessage);
      
      if (this._pendingPromise) {
        this._pendingPromise.reject(new Error(errorMessage));
        this._pendingPromise = null;
      }
    } catch (handlerError) {
      console.error('Error in popup error handler:', handlerError);
    }
  }
  
  // Load Google Identity Services script with retry logic
  async _loadGoogleScriptWithRetry() {
    for (let attempt = 0; attempt < this._maxRetries; attempt++) {
      try {
        await this._loadGoogleScript();
        return; // Success
      } catch (error) {
        console.warn(`Google script loading attempt ${attempt + 1} failed:`, error);
        if (attempt === this._maxRetries - 1) {
          throw error; // Final attempt failed
        }
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, attempt)));
      }
    }
  }
  
  // Load Google Identity Services script
  _loadGoogleScript() {
    return new Promise((resolve, reject) => {
      // Check if already loaded
      if (window.google?.accounts?.id) {
        resolve();
        return;
      }

      // Check if script is already loading
      const existingScript = document.querySelector('script[src*="gsi/client"]');
      if (existingScript) {
        // Script is loading, wait for it
        const checkInterval = 100;
        const maxWaitTime = 10000; // 10 seconds
        let waitTime = 0;
        
        const checkGoogleLoaded = setInterval(() => {
          waitTime += checkInterval;
          
          if (window.google?.accounts?.id) {
            clearInterval(checkGoogleLoaded);
            resolve();
          } else if (waitTime >= maxWaitTime) {
            clearInterval(checkGoogleLoaded);
            reject(new Error('Google script loading timeout'));
          }
        }, checkInterval);
        return;
      }

      const script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      
      script.onload = () => {
        // Wait a bit for Google APIs to initialize
        setTimeout(() => {
          if (window.google?.accounts?.id) {
            resolve();
          } else {
            reject(new Error('Google APIs not available after script load'));
          }
        }, 100);
      };
      
      script.onerror = (error) => {
        console.error('Google script loading error:', error);
        reject(new Error('Failed to load Google authentication script'));
      };
      
      document.head.appendChild(script);
    });
  }
}

export const googleAuth = new GoogleAuth();