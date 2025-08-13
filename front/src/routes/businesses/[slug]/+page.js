// src/routes/businesses/[slug]/+page.js
import { businessAPI } from '$lib/api/businesses';
import { error } from '@sveltejs/kit';

export async function load({ params }) {
  const { slug } = params;
  
  try {
    // Load business data
    const { data: business, error: businessError } = await businessAPI.get(slug);
    
    if (businessError || !business) {
      throw error(404, 'Business not found');
    }
    
    // Load additional data
    const [servicesResponse, reviewsResponse] = await Promise.all([
      businessAPI.getServices(business.slug),
      // For now, return empty reviews - we'll implement this later
      Promise.resolve({ data: [] })
    ]);
    
    return {
      business,
      services: servicesResponse.data?.results || [],
      reviews: reviewsResponse.data || []
    };
  } catch (err) {
    console.error('Error loading business data:', err);
    throw error(500, 'Failed to load business data');
  }
}