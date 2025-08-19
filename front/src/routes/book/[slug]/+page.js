import { redirect } from '@sveltejs/kit';
import { businessAPI } from '$lib/api/businesses';

export async function load({ params }) {
    const { slug } = params;
    
    try {
        const { data: business, error } = await businessAPI.get(slug);
        
        if (error || !business) {
            throw redirect(302, '/businesses');
        }

        // Get business services
        const { data: services, error: servicesError } = await businessAPI.getServices(slug);

        return {
            business,
            services: services || []
        };
    } catch (error) {
        console.error('Error loading business for booking:', error);
        throw redirect(302, '/businesses');
    }
}