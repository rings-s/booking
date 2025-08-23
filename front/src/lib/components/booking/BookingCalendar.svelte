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
    let isAnimating = $state(false);
    
    // Parse available dates if they come from API response
    let parsedAvailableDates = $derived(Array.isArray(availableDates) ? 
      (availableDates.length > 0 && typeof availableDates[0] === 'object' && availableDates[0].date ? 
        parseAvailableDates({ available_dates: availableDates }) : 
        availableDates.map(d => ({ date: d, dateString: d.toISOString().split('T')[0] }))
      ) : []);
    
    // Derive calendar days from current month
    let calendarDays = $derived(getCalendarDays(currentMonth));
    
    $effect(() => {
      isAnimating = true;
      setTimeout(() => {
        isAnimating = false;
      }, 150);
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
      const baseClasses = [
        'relative h-12 w-12 flex items-center justify-center text-sm font-medium rounded-xl',
        'transition-all duration-300 ease-in-out transform-gpu',
        'backdrop-blur-sm border border-white/10'
      ];
      
      if (isSameDay(date, selectedDate)) {
        baseClasses.push(
          'bg-gradient-to-br from-blue-500 to-purple-600 text-white shadow-xl shadow-blue-500/25',
          'scale-110 ring-4 ring-blue-500/30 border-white/20'
        );
      } else if (isDateDisabledForBooking(date)) {
        baseClasses.push(
          'bg-gray-100/50 text-gray-400 cursor-not-allowed',
          'border-gray-200/30'
        );
      } else if (isAvailable(date)) {
        baseClasses.push(
          'bg-gradient-to-br from-emerald-50 to-blue-50 text-emerald-700',
          'hover:bg-gradient-to-br hover:from-emerald-100 hover:to-blue-100',
          'hover:scale-105 hover:shadow-lg hover:shadow-emerald-500/20',
          'cursor-pointer border-emerald-200/50 hover:border-emerald-300/70'
        );
      } else if (isPast(date)) {
        baseClasses.push(
          'bg-gray-50/30 text-gray-400 cursor-not-allowed',
          'border-gray-200/20'
        );
      } else {
        baseClasses.push(
          'bg-white/30 text-gray-700 hover:bg-white/50',
          'hover:scale-105 hover:shadow-md cursor-pointer',
          'border-gray-200/40 hover:border-gray-300/60'
        );
      }
      
      if (isToday(date) && !isSameDay(date, selectedDate)) {
        baseClasses.push('ring-2 ring-orange-400/60 bg-gradient-to-br from-orange-50 to-yellow-50');
      }
      
      return baseClasses.join(' ');
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
  
<!-- Premium Calendar Container with Proper Centering -->
<div class="flex items-center justify-center min-h-[500px] p-4">
  <div class="w-full max-w-md mx-auto">
    <!-- Main Calendar Card with Glass Morphism -->
    <div class="relative backdrop-blur-xl bg-white/80 rounded-3xl shadow-2xl border border-white/20 overflow-hidden">
      <!-- Gradient Overlay -->
      <div class="absolute inset-0 bg-gradient-to-br from-blue-50/30 via-purple-50/20 to-pink-50/30 pointer-events-none"></div>
      
      <!-- Calendar Header -->
      <div class="relative z-10 flex items-center justify-between px-8 py-6 border-b border-white/20 bg-white/30 backdrop-blur-sm">
        <button
          type="button"
          class="group p-3 rounded-2xl bg-white/40 backdrop-blur-sm border border-white/30 hover:bg-white/60 hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
          onclick={previousMonth}
          disabled={loading}
          aria-label="Previous month"
        >
          <svg class="w-5 h-5 text-gray-700 group-hover:text-gray-900 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <div class="text-center flex-1">
          <h2 class="text-2xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent mb-1">
            {format(currentMonth, 'MMMM yyyy')}
          </h2>
          {#if parsedAvailableDates.length > 0}
            <div class="inline-flex items-center px-3 py-1 rounded-full bg-emerald-100/60 border border-emerald-200/50 backdrop-blur-sm">
              <div class="w-2 h-2 bg-emerald-500 rounded-full mr-2 animate-pulse"></div>
              <span class="text-xs font-medium text-emerald-700">
                {getAvailableDatesInMonth()} available this month
              </span>
            </div>
          {/if}
        </div>
        
        <button
          type="button"
          class="group p-3 rounded-2xl bg-white/40 backdrop-blur-sm border border-white/30 hover:bg-white/60 hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
          onclick={nextMonth}
          disabled={loading}
          aria-label="Next month"
        >
          <svg class="w-5 h-5 text-gray-700 group-hover:text-gray-900 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
      
      <!-- Calendar Body -->
      <div class="relative z-10 p-8">
        {#if loading}
          <div class="flex flex-col items-center justify-center py-12">
            <div class="relative">
              <div class="w-12 h-12 rounded-full border-4 border-blue-200 border-t-blue-500 animate-spin"></div>
              <div class="absolute inset-0 w-12 h-12 rounded-full border-4 border-transparent border-r-purple-500 animate-spin animation-delay-75"></div>
            </div>
            <span class="mt-4 text-gray-600 font-medium">Loading available dates...</span>
          </div>
        {:else}
          <!-- Day Headers -->
          <div class="grid grid-cols-7 gap-2 mb-4">
            {#each ['S', 'M', 'T', 'W', 'T', 'F', 'S'] as day, index}
              <div class="text-center text-xs font-bold text-gray-500 py-2 uppercase tracking-wider">
                <span class="hidden sm:inline">{['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][index]}</span>
                <span class="sm:hidden">{day}</span>
              </div>
            {/each}
          </div>
          
          <!-- Calendar Grid -->
          <div class="grid grid-cols-7 gap-2 {isAnimating ? 'opacity-50 scale-95' : 'opacity-100 scale-100'} transition-all duration-300">
            {#each calendarDays as date}
              <button
                type="button"
                class={getDateClasses(date)}
                disabled={isDateDisabledForBooking(date)}
                onclick={() => selectDate(date)}
                aria-label={`Select ${format(date, 'MMMM d, yyyy')}`}
              >
                <span class="relative z-10">{format(date, 'd')}</span>
                
                <!-- Available Date Indicator -->
                {#if isAvailable(date) && !isSameDay(date, selectedDate)}
                  <div class="absolute bottom-1 left-1/2 transform -translate-x-1/2 w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-sm"></div>
                {/if}
                
                <!-- Today Indicator -->
                {#if isToday(date) && !isSameDay(date, selectedDate)}
                  <div class="absolute top-1 right-1 w-2.5 h-2.5 bg-gradient-to-br from-orange-400 to-red-400 rounded-full shadow-sm"></div>
                {/if}
                
                <!-- Selected Date Glow -->
                {#if isSameDay(date, selectedDate)}
                  <div class="absolute inset-0 bg-gradient-to-br from-blue-400/20 to-purple-400/20 rounded-xl blur animate-pulse"></div>
                {/if}
              </button>
            {/each}
          </div>
          
          <!-- Empty State -->
          {#if parsedAvailableDates.length === 0 && !loading}
            <div class="text-center py-8">
              <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
                <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <p class="text-gray-600 font-medium mb-1">No available dates found</p>
              <p class="text-gray-400 text-sm">Try selecting a different service or time period</p>
            </div>
          {/if}
        {/if}
      </div>
      
      <!-- Premium Legend -->
      <div class="relative z-10 px-8 pb-6 border-t border-white/20 bg-white/20 backdrop-blur-sm">
        <div class="flex items-center justify-center space-x-6 text-xs">
          <div class="flex items-center group">
            <div class="w-4 h-4 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 mr-2 shadow-sm group-hover:scale-110 transition-transform"></div>
            <span class="font-medium text-gray-700">Selected</span>
          </div>
          <div class="flex items-center group">
            <div class="w-4 h-4 rounded-lg bg-gradient-to-br from-emerald-50 to-blue-50 border-2 border-emerald-200 mr-2 relative group-hover:scale-110 transition-transform">
              <div class="absolute bottom-0.5 left-1/2 transform -translate-x-1/2 w-1.5 h-1.5 bg-emerald-500 rounded-full"></div>
            </div>
            <span class="font-medium text-gray-700">Available</span>
          </div>
          <div class="flex items-center group">
            <div class="w-4 h-4 rounded-lg bg-gradient-to-br from-orange-50 to-yellow-50 border-2 border-orange-400 mr-2 relative group-hover:scale-110 transition-transform">
              <div class="absolute top-0.5 right-0.5 w-1.5 h-1.5 bg-orange-400 rounded-full"></div>
            </div>
            <span class="font-medium text-gray-700">Today</span>
          </div>
          <div class="flex items-center group">
            <div class="w-4 h-4 rounded-lg bg-gray-100 border-2 border-gray-200 mr-2 group-hover:scale-110 transition-transform"></div>
            <span class="font-medium text-gray-700">Unavailable</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  @keyframes animation-delay-75 {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  
  .animation-delay-75 {
    animation-delay: 75ms;
  }
</style>