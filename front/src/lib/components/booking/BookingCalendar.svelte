<!-- src/lib/components/booking/BookingCalendar.svelte -->
<script>
    import { 
      getCalendarDays, 
      isDateBookable, 
      isDateAvailable, 
      isDateDisabled, 
      parseAvailableDates 
    } from '$lib/utils/dates';
    import { format, isSameDay, isToday, isPast } from 'date-fns';
    
    let {
        selectedDate = $bindable(null),
        availableDates = [],
        businessHours = [],
        minDate = new Date(),
        maxDate = null,
        loading = false,
        ondateselect = () => {},
        ...restProps
    } = $props();
    
    let currentMonth = $state(new Date());
    let calendarDays = $state(getCalendarDays(currentMonth));
    
    // Parse available dates if they come from API response
    let parsedAvailableDates = $derived(Array.isArray(availableDates) ? 
      (availableDates.length > 0 && typeof availableDates[0] === 'object' && availableDates[0].date ? 
        parseAvailableDates({ available_dates: availableDates }) : 
        availableDates.map(d => ({ date: d, dateString: d.toISOString().split('T')[0] }))
      ) : []);
    
    $effect(() => {
      calendarDays = getCalendarDays(currentMonth);
    });
    
    function previousMonth() {
      const newMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1);
      // Don't go to past months
      if (newMonth.getFullYear() >= minDate.getFullYear() && 
          (newMonth.getFullYear() > minDate.getFullYear() || newMonth.getMonth() >= minDate.getMonth())) {
        currentMonth = newMonth;
      }
    }
    
    function nextMonth() {
      const newMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1);
      // Don't go beyond max date if set
      if (!maxDate || 
          (newMonth.getFullYear() <= maxDate.getFullYear() && 
           (newMonth.getFullYear() < maxDate.getFullYear() || newMonth.getMonth() <= maxDate.getMonth()))) {
        currentMonth = newMonth;
      }
    }
    
    function selectDate(date) {
      if (!isDateDisabledForBooking(date)) {
        selectedDate = date;
        ondateselect(date);
      }
    }
    
    function isAvailable(date) {
      return isDateAvailable(date, parsedAvailableDates);
    }
    
    function isDateDisabledForBooking(date) {
      return isDateDisabled(date, parsedAvailableDates, businessHours) || 
             (minDate && date < minDate) || 
             (maxDate && date > maxDate);
    }
    
    function getDateClasses(date) {
      const classes = ['relative py-3 text-sm rounded transition-colors'];
      
      if (isSameDay(date, selectedDate)) {
        classes.push('bg-indigo-600 text-white hover:bg-indigo-700');
      } else if (isDateDisabledForBooking(date)) {
        classes.push('text-gray-300 cursor-not-allowed');
      } else if (isAvailable(date)) {
        classes.push('text-indigo-600 hover:bg-indigo-50 cursor-pointer');
      } else if (isPast(date)) {
        classes.push('text-gray-400 cursor-not-allowed');
      } else {
        classes.push('text-gray-900 hover:bg-gray-100 cursor-pointer');
      }
      
      if (isToday(date)) {
        classes.push('font-semibold');
      }
      
      return classes.join(' ');
    }
    
    function getAvailableDatesInMonth() {
      if (!parsedAvailableDates.length) return 0;
      
      const monthStart = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), 1);
      const monthEnd = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0);
      
      return parsedAvailableDates.filter(dateItem => {
        const date = dateItem.date;
        return date >= monthStart && date <= monthEnd;
      }).length;
    }
  </script>
  
  <div class="bg-white rounded-lg shadow">
    <div class="flex items-center justify-between px-6 py-4 border-b">
      <button
        type="button"
        class="p-2 hover:bg-gray-100 rounded-full disabled:opacity-50 disabled:cursor-not-allowed"
        on:click={previousMonth}
        disabled={loading}
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      
      <div class="text-center">
        <h2 class="text-lg font-semibold text-gray-900">
          {format(currentMonth, 'MMMM yyyy')}
        </h2>
        {#if parsedAvailableDates.length > 0}
          <p class="text-xs text-gray-500">
            {getAvailableDatesInMonth()} available dates this month
          </p>
        {/if}
      </div>
      
      <button
        type="button"
        class="p-2 hover:bg-gray-100 rounded-full disabled:opacity-50 disabled:cursor-not-allowed"
        on:click={nextMonth}
        disabled={loading}
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
    
    <div class="p-6">
      {#if loading}
        <div class="flex items-center justify-center py-8">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
          <span class="ml-2 text-gray-600">Loading available dates...</span>
        </div>
      {:else}
        <div class="grid grid-cols-7 gap-1 mb-2">
          {#each ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] as day}
            <div class="text-center text-xs font-medium text-gray-500 py-2">
              {day}
            </div>
          {/each}
        </div>
        
        <div class="grid grid-cols-7 gap-1">
          {#each calendarDays as date}
            <button
              type="button"
              class={getDateClasses(date)}
              disabled={isDateDisabledForBooking(date)}
              on:click={() => selectDate(date)}
            >
              <span>{format(date, 'd')}</span>
              {#if isAvailable(date) && !isSameDay(date, selectedDate)}
                <span class="absolute bottom-1 left-1/2 transform -translate-x-1/2 w-1.5 h-1.5 bg-indigo-600 rounded-full"></span>
              {/if}
              {#if isToday(date) && !isSameDay(date, selectedDate)}
                <span class="absolute top-1 right-1 w-2 h-2 bg-blue-500 rounded-full"></span>
              {/if}
            </button>
          {/each}
        </div>
        
        {#if parsedAvailableDates.length === 0 && !loading}
          <div class="text-center py-4">
            <p class="text-gray-500 text-sm">No available dates found</p>
            <p class="text-gray-400 text-xs mt-1">Try selecting a different service or time period</p>
          </div>
        {/if}
      {/if}
    </div>
    
    <!-- Legend -->
    <div class="px-6 pb-4">
      <div class="flex items-center justify-center space-x-4 text-xs text-gray-600">
        <div class="flex items-center">
          <div class="w-3 h-3 bg-indigo-600 rounded mr-1"></div>
          <span>Selected</span>
        </div>
        <div class="flex items-center">
          <div class="w-3 h-3 border border-indigo-600 rounded mr-1 relative">
            <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-indigo-600 rounded-full"></div>
          </div>
          <span>Available</span>
        </div>
        <div class="flex items-center">
          <div class="w-3 h-3 bg-gray-300 rounded mr-1"></div>
          <span>Unavailable</span>
        </div>
      </div>
    </div>
  </div>