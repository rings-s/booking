// src/lib/utils/dates.js
import { 
    addDays, 
    addMinutes, 
    startOfDay, 
    endOfDay,
    startOfWeek,
    endOfWeek,
    startOfMonth,
    endOfMonth,
    isAfter,
    isBefore,
    isToday,
    isTomorrow,
    isPast,
    isFuture,
    differenceInMinutes,
    eachDayOfInterval,
    getDay
  } from 'date-fns';
  
  // Get available time slots for a service
  export function getTimeSlots(openTime, closeTime, duration, bufferTime = 0) {
    const slots = [];
    const [openHour, openMinute] = openTime.split(':').map(Number);
    const [closeHour, closeMinute] = closeTime.split(':').map(Number);
    
    const startDate = new Date();
    startDate.setHours(openHour, openMinute, 0, 0);
    
    const endDate = new Date();
    endDate.setHours(closeHour, closeMinute, 0, 0);
    
    let currentSlot = startDate;
    const slotDuration = duration + bufferTime;
    
    while (currentSlot < endDate) {
      const slotEnd = addMinutes(currentSlot, duration);
      if (slotEnd <= endDate) {
        slots.push({
          start: currentSlot.toTimeString().slice(0, 5),
          end: slotEnd.toTimeString().slice(0, 5)
        });
      }
      currentSlot = addMinutes(currentSlot, slotDuration);
    }
    
    return slots;
  }
  
  // Check if time slot is available
  export function isSlotAvailable(slot, existingBookings) {
    return !existingBookings.some(booking => {
      const bookingStart = booking.start_time;
      const bookingEnd = booking.end_time;
      return (
        (slot.start >= bookingStart && slot.start < bookingEnd) ||
        (slot.end > bookingStart && slot.end <= bookingEnd) ||
        (slot.start <= bookingStart && slot.end >= bookingEnd)
      );
    });
  }
  
  // Get calendar days for a month view
  export function getCalendarDays(date) {
    const start = startOfWeek(startOfMonth(date));
    const end = endOfWeek(endOfMonth(date));
    return eachDayOfInterval({ start, end });
  }
  
  // Check if business is open on a specific day
  export function isBusinessOpen(date, businessHours) {
    const dayOfWeek = getDay(date);
    const hours = businessHours.find(h => h.weekday === dayOfWeek);
    return hours && !hours.is_closed;
  }
  
  // Get next available date
  export function getNextAvailableDate(businessHours, maxDays = 30) {
    let date = new Date();
    
    for (let i = 0; i < maxDays; i++) {
      if (isBusinessOpen(date, businessHours)) {
        return date;
      }
      date = addDays(date, 1);
    }
    
    return null;
  }
  
  // Format date range
  export function formatDateRange(startDate, endDate) {
    const start = formatDate(startDate, 'MMM dd');
    const end = formatDate(endDate, 'MMM dd, yyyy');
    return `${start} - ${end}`;
  }
  
  // Check if date is bookable
  export function isDateBookable(date, minAdvanceTime = 0, maxAdvanceDays = 90, businessHours = []) {
    const now = new Date();
    const minDate = addMinutes(now, minAdvanceTime);
    const maxDate = addDays(now, maxAdvanceDays);
    
    const isInRange = isAfter(date, minDate) && isBefore(date, maxDate);
    
    // If business hours provided, check if business is open
    if (businessHours.length > 0) {
      return isInRange && isBusinessOpen(date, businessHours);
    }
    
    return isInRange;
  }
  
  // Get business hours for a specific day
  export function getBusinessHoursForDay(date, businessHours) {
    const dayOfWeek = getDay(date);
    return businessHours.find(h => h.weekday === dayOfWeek);
  }
  
  // Parse time string to Date object
  export function parseTime(timeString, baseDate = new Date()) {
    const [hours, minutes] = timeString.split(':').map(Number);
    const date = new Date(baseDate);
    date.setHours(hours, minutes, 0, 0);
    return date;
  }
  
  // Calculate booking end time
  export function calculateEndTime(startTime, durationMinutes) {
    const start = parseTime(startTime);
    return addMinutes(start, durationMinutes);
  }

  // Convert available dates from API response to Date objects
  export function parseAvailableDates(availableDatesResponse) {
    if (!availableDatesResponse || !availableDatesResponse.available_dates) {
      return [];
    }
    
    return availableDatesResponse.available_dates.map(dateItem => ({
      date: new Date(dateItem.date),
      weekday: dateItem.weekday,
      slotsCount: dateItem.slots_count,
      dateString: dateItem.date
    }));
  }

  // Check if a specific date is in the available dates list
  export function isDateAvailable(date, availableDates) {
    if (!availableDates || availableDates.length === 0) return false;
    
    const dateString = date.toISOString().split('T')[0]; // Get YYYY-MM-DD format
    return availableDates.some(availableDate => 
      availableDate.dateString === dateString || 
      availableDate.date.toDateString() === date.toDateString()
    );
  }

  // Get available dates for calendar display
  export function getAvailableDatesForCalendar(availableDatesResponse) {
    const parsed = parseAvailableDates(availableDatesResponse);
    return parsed.map(item => item.date);
  }

  // Check if date should be disabled in calendar
  export function isDateDisabled(date, availableDates = [], businessHours = []) {
    // Check if date is in the past
    if (isPast(date) && !isToday(date)) {
      return true;
    }
    
    // Check if business is closed on this day
    if (businessHours.length > 0 && !isBusinessOpen(date, businessHours)) {
      return true;
    }
    
    // Check if date is not in available dates list
    if (availableDates.length > 0 && !isDateAvailable(date, availableDates)) {
      return true;
    }
    
    return false;
  }

  // Get next available business day
  export function getNextBusinessDay(businessHours, startDate = new Date()) {
    let currentDate = startDate;
    const maxDays = 365; // Prevent infinite loop
    let daysChecked = 0;
    
    while (daysChecked < maxDays) {
      if (isBusinessOpen(currentDate, businessHours) && !isPast(currentDate)) {
        return currentDate;
      }
      currentDate = addDays(currentDate, 1);
      daysChecked++;
    }
    
    return null;
  }

  // Format business hours for display
  export function formatBusinessHours(businessHours) {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    
    return businessHours.map(hour => ({
      day: days[hour.weekday],
      hours: hour.is_closed ? 'Closed' : `${hour.opening_time} - ${hour.closing_time}`,
      isClosed: hour.is_closed
    }));
  }