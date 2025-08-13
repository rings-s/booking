// src/routes/bookings/[id]/+page.js
import { bookingAPI } from '$lib/api/bookings';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
  const { id } = params;
  
  try {
    const { data: booking, error: bookingError } = await bookingAPI.get(id);
    
    if (bookingError || !booking) {
      throw error(404, 'Booking not found');
    }
    
    return {
      booking
    };
  } catch (err) {
    console.error('Error loading booking data:', err);
    throw error(500, 'Failed to load booking data');
  }
}