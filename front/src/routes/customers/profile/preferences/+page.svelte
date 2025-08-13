<!-- src/routes/customers/preferences/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { customerAPI } from '$lib/api/customers';
    import { notificationAPI } from '$lib/api/notifications';
    import { auth } from '$lib/stores/auth';
    import Button from '$lib/components/common/Button.svelte';
    import Card from '$lib/components/common/Card.svelte';
    import Alert from '$lib/components/common/Alert.svelte';
    import Spinner from '$lib/components/common/Spinner.svelte';
    import toast from 'svelte-french-toast';
    
    let loading = true;
    let saving = false;
    let preferences = null;
    let testingSMS = false;
    let testingEmail = false;
    
    // Notification preferences
    let notifications = {
      booking_confirmation: {
        email: true,
        sms: false,
        push: false
      },
      booking_reminder: {
        email: true,
        sms: true,
        push: true
      },
      booking_changes: {
        email: true,
        sms: true,
        push: true
      },
      payment_receipts: {
        email: true,
        sms: false,
        push: false
      },
      review_requests: {
        email: true,
        sms: false,
        push: false
      },
      promotional: {
        email: false,
        sms: false,
        push: false
      },
      newsletter: {
        email: false,
        sms: false,
        push: false
      }
    };
    
    // Communication preferences
    let communication = {
      preferred_language: 'en',
      timezone: 'America/New_York',
      date_format: 'MM/DD/YYYY',
      time_format: '12h',
      reminder_timing: 24, // hours before appointment
      quiet_hours_enabled: false,
      quiet_hours_start: '21:00',
      quiet_hours_end: '09:00'
    };
    
    // Privacy settings
    let privacy = {
      show_profile_photo: true,
      show_booking_history: false,
      allow_reviews: true,
      data_sharing: false,
      analytics_tracking: true,
      third_party_marketing: false
    };
    
    // Contact preferences
    let contact = {
      preferred_contact_method: 'email',
      email_frequency: 'immediate',
      sms_enabled: false,
      phone_verified: false,
      email_verified: true,
      backup_email: '',
      backup_phone: ''
    };
    
    const languages = [
      { value: 'en', label: 'English' },
      { value: 'es', label: 'Spanish' },
      { value: 'fr', label: 'French' },
      { value: 'de', label: 'German' },
      { value: 'pt', label: 'Portuguese' },
      { value: 'zh', label: 'Chinese' }
    ];
    
    const timezones = [
      { value: 'America/New_York', label: 'Eastern Time (ET)' },
      { value: 'America/Chicago', label: 'Central Time (CT)' },
      { value: 'America/Denver', label: 'Mountain Time (MT)' },
      { value: 'America/Los_Angeles', label: 'Pacific Time (PT)' },
      { value: 'America/Phoenix', label: 'Arizona Time' },
      { value: 'Pacific/Honolulu', label: 'Hawaii Time' }
    ];
    
    const emailFrequencies = [
      { value: 'immediate', label: 'Immediately' },
      { value: 'daily', label: 'Daily Digest' },
      { value: 'weekly', label: 'Weekly Summary' },
      { value: 'never', label: 'Never' }
    ];
    
    const reminderTimings = [
      { value: 1, label: '1 hour before' },
      { value: 2, label: '2 hours before' },
      { value: 4, label: '4 hours before' },
      { value: 12, label: '12 hours before' },
      { value: 24, label: '24 hours before' },
      { value: 48, label: '48 hours before' }
    ];
    
    onMount(async () => {
      await loadPreferences();
    });
    
    async function loadPreferences() {
      loading = true;
      
      const { data, error } = await customerAPI.getPreferences();
      
      if (data) {
        preferences = data;
        
        // Map loaded preferences to local state
        if (data.notifications) {
          notifications = { ...notifications, ...data.notifications };
        }
        if (data.communication) {
          communication = { ...communication, ...data.communication };
        }
        if (data.privacy) {
          privacy = { ...privacy, ...data.privacy };
        }
        if (data.contact) {
          contact = { ...contact, ...data.contact };
        }
      }
      
      loading = false;
    }
    
    async function savePreferences() {
      saving = true;
      
      const payload = {
        notifications,
        communication,
        privacy,
        contact
      };
      
      const { data, error } = await customerAPI.updatePreferences(payload);
      
      if (data) {
        preferences = data;
        toast.success('Preferences saved successfully');
      } else {
        toast.error(error || 'Failed to save preferences');
      }
      
      saving = false;
    }
    
    async function testEmailNotification() {
      testingEmail = true;
      
      const { data, error } = await notificationAPI.sendTestEmail();
      
      if (data) {
        toast.success('Test email sent! Check your inbox.');
      } else {
        toast.error('Failed to send test email');
      }
      
      testingEmail = false;
    }
    
    async function testSMSNotification() {
      if (!contact.sms_enabled || !contact.phone_verified) {
        toast.error('Please enable and verify SMS first');
        return;
      }
      
      testingSMS = true;
      
      const { data, error } = await notificationAPI.sendTestSMS();
      
      if (data) {
        toast.success('Test SMS sent! Check your phone.');
      } else {
        toast.error('Failed to send test SMS');
      }
      
      testingSMS = false;
    }
    
    async function verifyPhone() {
      const { data, error } = await customerAPI.sendPhoneVerification();
      
      if (data) {
        toast.success('Verification code sent to your phone');
        // Show verification modal
      } else {
        toast.error('Failed to send verification code');
      }
    }
    
    async function unsubscribeAll() {
      if (!confirm('Are you sure you want to unsubscribe from all communications? You will still receive essential service notifications.')) {
        return;
      }
      
      // Set all non-essential notifications to false
      Object.keys(notifications).forEach(key => {
        if (key === 'promotional' || key === 'newsletter') {
          notifications[key] = { email: false, sms: false, push: false };
        }
      });
      
      await savePreferences();
    }
    
    function toggleAllNotifications(type, enabled) {
      Object.keys(notifications[type]).forEach(channel => {
        notifications[type][channel] = enabled;
      });
    }
    
    // Check if user has any critical notifications disabled
    $: hasDisabledCritical = !notifications.booking_confirmation.email || 
                             !notifications.booking_changes.email;
  </script>
  
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="py-6 flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Notification Preferences</h1>
            <p class="mt-1 text-sm text-gray-600">
              Manage how and when you receive notifications
            </p>
          </div>
          
          <Button on:click={savePreferences} loading={saving}>
            Save Changes
          </Button>
        </div>
      </div>
    </div>
    
    {#if loading}
      <div class="flex justify-center py-12">
        <Spinner size="lg">Loading preferences...</Spinner>
      </div>
    {:else}
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Main Content -->
          <div class="lg:col-span-2 space-y-6">
            <!-- Notification Settings -->
            <Card title="Notification Settings">
              {#if hasDisabledCritical}
                <Alert type="warning" class="mb-4">
                  You have disabled critical notifications. You may miss important updates about your bookings.
                </Alert>
              {/if}
              
              <div class="space-y-6">
                {#each Object.entries(notifications) as [key, channels]}
                  {@const title = key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                  {@const isEssential = ['booking_confirmation', 'booking_changes', 'payment_receipts'].includes(key)}
                  
                  <div class="border-b border-gray-200 pb-4 last:border-0">
                    <div class="flex items-center justify-between mb-3">
                      <div>
                        <h4 class="text-sm font-medium text-gray-900">
                          {title}
                          {#if isEssential}
                            <span class="ml-2 text-xs text-gray-500">(Essential)</span>
                          {/if}
                        </h4>
                      </div>
                      
                      <button
                        type="button"
                        class="text-xs text-indigo-600 hover:text-indigo-500"
                        on:click={() => toggleAllNotifications(key, !channels.email)}
                      >
                        {channels.email ? 'Disable all' : 'Enable all'}
                      </button>
                    </div>
                    
                    <div class="grid grid-cols-3 gap-4">
                      <label class="flex items-center">
                        <input
                          type="checkbox"
                          bind:checked={channels.email}
                          class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                        />
                        <span class="ml-2 text-sm text-gray-700">Email</span>
                      </label>
                      
                      <label class="flex items-center">
                        <input
                          type="checkbox"
                          bind:checked={channels.sms}
                          disabled={!contact.sms_enabled}
                          class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded disabled:opacity-50"
                        />
                        <span class="ml-2 text-sm text-gray-700 {!contact.sms_enabled ? 'opacity-50' : ''}">
                          SMS
                        </span>
                      </label>
                      
                      <label class="flex items-center">
                        <input
                          type="checkbox"
                          bind:checked={channels.push}
                          class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                        />
                        <span class="ml-2 text-sm text-gray-700">Push</span>
                      </label>
                    </div>
                  </div>
                {/each}
              </div>
            </Card>
            
            <!-- Communication Preferences -->
            <Card title="Communication Preferences">
              <div class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Preferred Language
                    </label>
                    <select
                      bind:value={communication.preferred_language}
                      class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                      {#each languages as lang}
                        <option value={lang.value}>{lang.label}</option>
                      {/each}
                    </select>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Timezone
                    </label>
                    <select
                      bind:value={communication.timezone}
                      class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                      {#each timezones as tz}
                        <option value={tz.value}>{tz.label}</option>
                      {/each}
                    </select>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Date Format
                    </label>
                    <select
                      bind:value={communication.date_format}
                      class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                      <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                      <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                      <option value="YYYY-MM-DD">YYYY-MM-DD</option>
                    </select>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Time Format
                    </label>
                    <select
                      bind:value={communication.time_format}
                      class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                      <option value="12h">12-hour (AM/PM)</option>
                      <option value="24h">24-hour</option>
                    </select>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Reminder Timing
                    </label>
                    <select
                      bind:value={communication.reminder_timing}
                      class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                      {#each reminderTimings as timing}
                        <option value={timing.value}>{timing.label}</option>
                      {/each}
                    </select>
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                      Email Frequency
                    </label>
                    <select
                      bind:value={contact.email_frequency}
                      class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                    >
                      {#each emailFrequencies as freq}
                        <option value={freq.value}>{freq.label}</option>
                      {/each}
                    </select>
                  </div>
                </div>
                
                <!-- Quiet Hours -->
                <div class="border-t border-gray-200 pt-4">
                  <label class="flex items-center">
                    <input
                      type="checkbox"
                      bind:checked={communication.quiet_hours_enabled}
                      class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    />
                    <span class="ml-2 text-sm font-medium text-gray-700">
                      Enable Quiet Hours
                    </span>
                  </label>
                  
                  {#if communication.quiet_hours_enabled}
                    <div class="mt-3 grid grid-cols-2 gap-4">
                      <div>
                        <label class="block text-sm text-gray-600 mb-1">
                          Start Time
                        </label>
                        <input
                          type="time"
                          bind:value={communication.quiet_hours_start}
                          class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        />
                      </div>
                      
                      <div>
                        <label class="block text-sm text-gray-600 mb-1">
                          End Time
                        </label>
                        <input
                          type="time"
                          bind:value={communication.quiet_hours_end}
                          class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                        />
                      </div>
                    </div>
                    
                    <p class="mt-2 text-xs text-gray-500">
                      Non-urgent notifications will be held during quiet hours
                    </p>
                  {/if}
                </div>
              </div>
            </Card>
            
            <!-- Privacy Settings -->
            <Card title="Privacy Settings">
              <div class="space-y-4">
                <label class="flex items-center justify-between">
                  <span class="text-sm text-gray-700">Show profile photo to businesses</span>
                  <input
                    type="checkbox"
                    bind:checked={privacy.show_profile_photo}
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                </label>
                
                <label class="flex items-center justify-between">
                  <span class="text-sm text-gray-700">Show booking history to businesses</span>
                  <input
                    type="checkbox"
                    bind:checked={privacy.show_booking_history}
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                </label>
                
                <label class="flex items-center justify-between">
                  <span class="text-sm text-gray-700">Allow businesses to request reviews</span>
                  <input
                    type="checkbox"
                    bind:checked={privacy.allow_reviews}
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                </label>
                
                <label class="flex items-center justify-between">
                  <span class="text-sm text-gray-700">Share data for service improvement</span>
                  <input
                    type="checkbox"
                    bind:checked={privacy.data_sharing}
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                </label>
                
                <label class="flex items-center justify-between">
                  <span class="text-sm text-gray-700">Analytics tracking</span>
                  <input
                    type="checkbox"
                    bind:checked={privacy.analytics_tracking}
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                </label>
                
                <label class="flex items-center justify-between">
                  <span class="text-sm text-gray-700">Third-party marketing</span>
                  <input
                    type="checkbox"
                    bind:checked={privacy.third_party_marketing}
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                </label>
              </div>
            </Card>
          </div>
          
          <!-- Sidebar -->
          <div class="space-y-6">
            <!-- Contact Methods -->
            <Card title="Contact Methods">
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    Preferred Contact Method
                  </label>
                  <select
                    bind:value={contact.preferred_contact_method}
                    class="block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  >
                    <option value="email">Email</option>
                    <option value="sms" disabled={!contact.sms_enabled}>SMS</option>
                    <option value="phone">Phone Call</option>
                    <option value="push">Push Notification</option>
                  </select>
                </div>
                
                <!-- SMS Settings -->
                <div class="border-t border-gray-200 pt-4">
                  <div class="flex items-center justify-between mb-3">
                    <label class="flex items-center">
                      <input
                        type="checkbox"
                        bind:checked={contact.sms_enabled}
                        class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                      />
                      <span class="ml-2 text-sm font-medium text-gray-700">
                        Enable SMS Notifications
                      </span>
                    </label>
                  </div>
                  
                  {#if contact.sms_enabled}
                    <div class="space-y-3">
                      {#if !contact.phone_verified}
                        <Alert type="warning">
                          <div class="flex items-center justify-between">
                            <span class="text-sm">Phone number not verified</span>
                            <Button size="sm" on:click={verifyPhone}>
                              Verify
                            </Button>
                          </div>
                        </Alert>
                      {:else}
                        <div class="flex items-center text-sm text-green-600">
                          <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                          </svg>
                          Phone verified
                        </div>
                      {/if}
                    </div>
                  {/if}
                </div>
                
                <!-- Test Notifications -->
                <div class="border-t border-gray-200 pt-4">
                  <h4 class="text-sm font-medium text-gray-700 mb-3">Test Notifications</h4>
                  
                  <div class="space-y-2">
                    <Button
                      fullWidth
                      variant="outline"
                      size="sm"
                      on:click={testEmailNotification}
                      loading={testingEmail}
                    >
                      Send Test Email
                    </Button>
                    
                    <Button
                      fullWidth
                      variant="outline"
                      size="sm"
                      on:click={testSMSNotification}
                      loading={testingSMS}
                      disabled={!contact.sms_enabled || !contact.phone_verified}
                    >
                      Send Test SMS
                    </Button>
                  </div>
                </div>
              </div>
            </Card>
            
            <!-- Quick Actions -->
            <Card title="Quick Actions">
              <div class="space-y-3">
                <Button
                  fullWidth
                  variant="outline"
                  on:click={unsubscribeAll}
                >
                  Unsubscribe from Marketing
                </Button>
                
                <Button
                  fullWidth
                  variant="outline"
                  href="/customers/profile"
                >
                  Edit Profile
                </Button>
                
                <Button
                  fullWidth
                  variant="outline"
                  href="/help/notifications"
                >
                  Help & Support
                </Button>
              </div>
            </Card>
            
            <!-- Info Box -->
            <Alert type="info">
              <h4 class="text-sm font-medium mb-2">About Notifications</h4>
              <p class="text-sm">
                Essential notifications about your bookings and payments cannot be disabled.
                You can control how you receive them using the options above.
              </p>
            </Alert>
          </div>
        </div>
      </div>
    {/if}
  </div>