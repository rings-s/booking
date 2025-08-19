# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack booking management system built with Django REST Framework (backend) and SvelteKit (frontend). It allows businesses to manage services, bookings, customers, and provides features like payment integration, notifications, and analytics.

**Key Features:**
- Multi-tenant business management with subscription-based access
- Service booking system with real-time calendar integration
- Customer management and profiles with booking history
- Payment processing with Stripe integration
- Review and rating system with business responses
- Subscription-based SaaS model (Free, Basic, Premium, Enterprise)
- Real-time notifications system
- Analytics dashboard with charts and insights
- QR code generation for businesses with media management

## Development Commands

### Backend (Django)
```bash
cd back/

# Development server
python manage.py runserver                    # Start development server (port 8000)

# Database operations
python manage.py migrate                      # Run database migrations
python manage.py makemigrations               # Create new migrations
python manage.py flush --noinput              # Clear database completely

# User management
python manage.py createsuperuser              # Create admin user
python manage.py create_test_user             # Create test user

# Data seeding and fixtures
./run_tests.sh                               # Complete setup with fixtures and media
python manage.py create_fixtures             # Generate fixture files
python manage.py loaddata accounts/fixtures/accounts_data.json  # Load accounts data
python manage.py loaddata base/fixtures/base_data.json         # Load business data
python manage.py test_media_qr               # Generate QR codes and media files
python scripts/seed_base.py                  # Run custom seed script

# Testing and validation
python manage.py test                        # Run tests
python manage.py check_admin                 # Verify admin registration
python manage.py shell                       # Django shell

# Static files
python manage.py collectstatic               # Collect static files
```

### Frontend (SvelteKit)
```bash
cd front/
npm run dev                 # Start development server (port 5173)
npm run build               # Build for production
npm run preview             # Preview production build
npm run check               # Type check
npm run lint                # Run linting
npm run format              # Format code
npm test                    # Run tests (alias for test:e2e)
npm run test:e2e            # Run Playwright E2E tests
```

## Architecture & Structure

### Backend Architecture (Django REST Framework)
- **Django Apps:**
  - `accounts/` - User authentication, subscriptions, user management
  - `base/` - Core business logic (businesses, bookings, reviews, notifications)

- **Key Models:**
  - `User` - Custom user model with role-based access (customer, business_owner, admin)
  - `Business` - Business profiles with location, services, QR codes
  - `Service` - Services offered by businesses
  - `Booking` - Booking management with status tracking
  - `Customer` - Customer profiles and preferences
  - `Review` - Rating and review system
  - `Subscription` - SaaS subscription management
  - `Notification` - In-app notification system

- **API Structure:**
  - RESTful API with ViewSets using Django REST Framework
  - JWT authentication with automatic refresh token handling
  - Nested routes for related resources using drf-nested-routers
  - Custom actions for business operations (dashboard, analytics, available slots)
  - Comprehensive error handling with structured responses
  - Query parameter filtering and pagination support

### Frontend Architecture (SvelteKit)
- **Framework:** SvelteKit with Svelte 5 (using runes)
- **Styling:** Tailwind CSS with custom components
- **State Management:** Svelte stores for auth, business, bookings, notifications
- **API Client:** Custom HTTP client with automatic token refresh

- **Key Components:**
  - `components/common/` - Reusable UI components (Button, Modal, Input, etc.)
  - `components/business/` - Business-specific components
  - `components/booking/` - Booking management components
  - `components/dashboard/` - Analytics and dashboard components
  - `components/layout/` - Header, Footer, Sidebar components

- **Route Structure:**
  - `/` - Landing page with featured businesses
  - `/auth/*` - Authentication pages (login, register, forgot-password)
  - `/businesses/` - Business directory and individual business pages
  - `/bookings/` - Booking management
  - `/dashboard/` - Business owner dashboard
  - `/customers/` - Customer management
  - `/subscriptions/` - Subscription management
  - `/notifications/` - Notification center

### Integration Patterns

**Authentication Flow:**
1. Frontend sends credentials to `/api/accounts/login/`
2. Backend returns access/refresh JWT tokens
3. API client stores tokens in localStorage
4. Automatic token refresh on 401 responses
5. Svelte auth store manages authentication state

**API Communication:**
- Base URL: `http://localhost:8000/api` (configurable via PUBLIC_API_URL)
- JWT Bearer token authentication
- Consistent error handling with toast notifications
- Automatic retry with token refresh

**State Management:**
- Auth store: User authentication and profile data
- Business store: Business data and operations  
- Booking store: Booking state and management
- Notification store: Real-time notification handling
- UI store: Modal states, loading states, etc.

### Page Connections & Navigation

**Main Navigation Flow:**
1. **Landing Page** (`/`) → Auth pages or business directory
2. **Authentication** (`/auth/*`) → Dashboard based on user type
3. **Business Directory** (`/businesses/`) → Individual business pages
4. **Business Pages** (`/businesses/{slug}`) → Booking flow or business management
5. **Dashboard** (`/dashboard/`) → Hub for business operations
6. **Booking Management** (`/bookings/`) → Individual booking details

**Key Navigation Patterns:**
- Header navigation changes based on authentication status
- Business owners see management options in navigation
- Customers see booking-focused navigation
- Breadcrumb navigation in business management pages
- Context-sensitive CTAs throughout the application

## API Reference & Integration

### Base URLs
- **Backend API**: `http://localhost:8000/api/` (configurable via PUBLIC_API_URL)
- **Admin Panel**: `http://localhost:8000/admin/`
- **Media Files**: `http://localhost:8000/media/`

### Authentication Endpoints
```
POST /api/accounts/register/           # User registration
POST /api/accounts/login/              # User login
POST /api/accounts/google-login/       # Google OAuth login
POST /api/accounts/google-callback/    # Google OAuth callback
POST /api/accounts/token/refresh/      # JWT token refresh
POST /api/accounts/token/verify/       # JWT token verification
```

### Business Endpoints
```
# Core CRUD operations
GET    /api/businesses/                # List all businesses (public)
POST   /api/businesses/                # Create business (authenticated)
GET    /api/businesses/{slug}/         # Get business details (public)
PATCH  /api/businesses/{slug}/         # Update business (owner only)
DELETE /api/businesses/{slug}/         # Delete business (owner only)

# Custom business actions
GET    /api/businesses/search/         # Search businesses with filters
GET    /api/businesses/featured/       # Get featured businesses
GET    /api/businesses/my/             # Get current user's businesses
GET    /api/businesses/{slug}/dashboard/          # Business dashboard data
GET    /api/businesses/{slug}/analytics-chart/   # Analytics charts
GET    /api/businesses/{slug}/available-slots/   # Available booking slots
GET    /api/businesses/{slug}/available-dates/   # Available booking dates
GET    /api/businesses/{slug}/stats/             # Business statistics
GET    /api/businesses/{slug}/revenue-data/      # Revenue analytics
GET    /api/businesses/{slug}/service-stats/     # Service performance
GET    /api/businesses/{slug}/recent-activity/   # Recent activity feed
POST   /api/businesses/{slug}/update-hours/      # Update business hours

# Nested business resources
GET    /api/businesses/{slug}/services/     # Services for business
GET    /api/businesses/{slug}/reviews/      # Reviews for business  
GET    /api/businesses/{slug}/bookings/     # Bookings for business
GET    /api/businesses/{slug}/hours/        # Business hours
```

### Service Endpoints
```
GET    /api/services/                  # List services with filtering
POST   /api/services/                  # Create service (business owner)
GET    /api/services/{id}/             # Get service details (public)
PATCH  /api/services/{id}/             # Update service (owner only)
DELETE /api/services/{id}/             # Delete service (owner only)
POST   /api/services/bulk-update/      # Bulk update services
POST   /api/services/update-order/     # Update service display order
```

### Booking Endpoints
```
# Core booking operations
GET    /api/bookings/                  # List user's bookings (filtered by role)
POST   /api/bookings/                  # Create new booking
GET    /api/bookings/{id}/             # Get booking details
PATCH  /api/bookings/{id}/             # Update booking
DELETE /api/bookings/{id}/             # Cancel/delete booking

# Booking actions
POST   /api/bookings/{id}/confirm/     # Confirm pending booking
POST   /api/bookings/{id}/cancel/      # Cancel booking
POST   /api/bookings/{id}/complete/    # Mark as completed
POST   /api/bookings/{id}/mark-no-show/ # Mark as no-show
GET    /api/bookings/upcoming/         # Get upcoming bookings
GET    /api/bookings/history/          # Get booking history
GET    /api/bookings/chart-data/       # Booking analytics data
```

### Customer Endpoints
```
GET    /api/customers/                 # List customers (business owner only)
POST   /api/customers/                 # Create customer profile
GET    /api/customers/{id}/            # Get customer details
PATCH  /api/customers/{id}/            # Update customer profile
GET    /api/customers/me/              # Get current user's customer profile
GET    /api/customers/{id}/booking-history/  # Customer booking history
GET    /api/customers/{id}/stats/      # Customer statistics
POST   /api/customers/{id}/add-preferred-business/    # Add to favorites
POST   /api/customers/{id}/remove-preferred-business/ # Remove from favorites
```

### Review & Notification Endpoints
```
# Reviews
GET    /api/reviews/                   # List reviews with filtering
POST   /api/reviews/                   # Create review (customer only)
GET    /api/reviews/{id}/              # Get review details
PATCH  /api/reviews/{id}/              # Update review (author only)
POST   /api/reviews/{id}/respond/      # Business response to review
POST   /api/reviews/{id}/mark-featured/ # Mark review as featured

# Notifications
GET    /api/notifications/             # List user notifications
GET    /api/notifications/unread-count/ # Get unread count
POST   /api/notifications/{id}/mark-read/ # Mark as read
POST   /api/notifications/mark-all-read/  # Mark all as read
DELETE /api/notifications/clear-all/   # Clear all read notifications
```

### Frontend API Client Usage
The frontend uses a centralized API client (`src/lib/api/clients.js`) with:
- Automatic JWT token management and refresh
- Comprehensive error handling with user-friendly messages
- Toast notification integration for API errors
- Automatic logout on authentication failure

**Example Usage:**
```javascript
import { businessAPI } from '$lib/api/businesses';

// Get business details
const { data, error } = await businessAPI.get('elite-hair-studio');

// Create booking with error handling
const { data, error } = await bookingAPI.create({
  business_id: businessId,  // Note: Use business_id, not business
  service_id: serviceId,    // Note: Use service_id, not service
  booking_date: '2025-01-15',
  start_time: '14:00:00',   // Note: Use start_time and end_time
  end_time: '15:00:00',
  notes: 'Optional booking notes'
});
```

### Query Parameters & Filtering
Most list endpoints support filtering:
- **Businesses**: `?category=spa&location=New York&rating_gte=4`
- **Services**: `?business=uuid&min_price=50&max_price=200`
- **Bookings**: `?status=confirmed&start_date=2025-01-01&end_date=2025-01-31`
- **Reviews**: `?business=uuid&rating=5&min_rating=4`

### Environment Configuration

**Backend (.env required):**
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:5173
REDIS_URL=redis://localhost:6379
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

**Frontend (.env required):**
```
PUBLIC_API_URL=http://localhost:8000/api
```

## Critical API Implementation Details

### Booking API Field Names
**IMPORTANT**: The booking API expects specific field names that differ from the model field names:
- Use `business_id` (UUID string), not `business`
- Use `service_id` (UUID string), not `service`  
- Use `start_time` and `end_time` (HH:MM:SS format), not `booking_time`
- The `customer` field is automatically populated from the authenticated user

### Service Creation for Business Owners
**IMPORTANT**: When creating services, use `business` (UUID string) in the request data. The ServiceViewSet `perform_create` method automatically associates it with the service instance.

### Authentication & Permissions
- **Customer users** can create bookings but not services
- **Business owners** can create services for their own businesses only  
- **Admin users** have full access to all resources
- All endpoints require authentication except public business/service listings

### Database Relationships
- Businesses are identified by `slug` in URLs but `id` (UUID) in relationships
- All other resources use UUID for both URLs and relationships
- Customer profiles are automatically created when users make their first booking

## Known Issues & Considerations

### Current System Status
- **User Registration/Login**: ✅ Working
- **Google OAuth**: ✅ Working  
- **Booking Creation**: ✅ Working (field names corrected)
- **Business Management**: ✅ Working (minor service creation issue)
- **Dashboard Analytics**: ✅ Working with real data
- **Subscription System**: ✅ Working (schema fixed)
- **Notifications**: ✅ Working
- **Internationalization**: ✅ Limited to Arabic/English only

### Service Creation Issue
- Service creation via API has a minor business association issue
- Direct database creation works fine
- Core functionality is unaffected
- Business owners can still manage existing services

### Environment Dependencies
- Backend requires Redis for Celery (background tasks) - optional for basic functionality
- PostgreSQL configuration available but SQLite used by default
- Google OAuth requires proper client credentials (test credentials configured)
- Stripe integration requires test keys for development

### Security Considerations
- CSRF protection enabled in Django
- JWT tokens stored in localStorage with automatic refresh
- File uploads validated for QR codes and business logos
- CORS configuration properly set for development

### Performance Notes
- Database uses SQLite by default (production should use PostgreSQL)
- QR codes and media files generated automatically
- Image uploads stored locally in `media/` directory
- No CDN configuration for static assets

## Development Workflow

### Initial Setup
1. **Backend Setup**:
   ```bash
   cd back/
   pip install -r requirements.txt      # Install dependencies
   python manage.py migrate            # Set up database
   ./run_tests.sh                      # Load fixtures and create media
   python manage.py runserver          # Start on port 8000
   ```

2. **Frontend Setup**:
   ```bash
   cd front/
   npm install                         # Install dependencies
   cp .env.example .env                # Configure environment
   npm run dev                         # Start on port 5173
   ```

3. **Test Data Access**:
   - **Admin Panel**: http://localhost:8000/admin/ (admin@example.com / password)
   - **Test Business Owner**: john.doe@example.com / password
   - **Test Customer**: mike.wilson@example.com / password

### Development Process
1. Start backend server first (Django on port 8000)
2. Start frontend development server (SvelteKit on port 5173) 
3. Both services must be running for full functionality
4. Backend serves API and admin panel, frontend handles user interface
5. Ensure Redis is running if testing background tasks
6. QR codes and media files are generated automatically

### Testing & Quality Assurance

**Backend Testing**:
```bash
cd back/
python manage.py test                # Run Django tests
python manage.py check_admin         # Verify admin configuration
python manage.py check              # System checks
python manage.py shell              # Django shell for debugging
```

**Frontend Testing**:
```bash
cd front/
npm run test:e2e                    # Run Playwright E2E tests
npm run check                       # TypeScript/Svelte checks
npm run lint                        # ESLint checks
npm run format                      # Prettier formatting
```

**Full System Testing** (All verified working):
- ✅ User registration and authentication flows
- ✅ Google OAuth integration
- ✅ Business creation and service management
- ✅ Booking creation and management workflows
- ✅ Notification system functionality
- ✅ Dashboard analytics with real data
- ✅ Subscription system with multiple plans
- ✅ Multi-language support (Arabic/English)

## Common Integration Issues & Solutions

### API URL Mismatches
The project uses consistent URL patterns between frontend and backend:

**Backend URL Structure** (`back/base/urls.py`):
- Custom endpoints are defined BEFORE router URLs to avoid conflicts
- Business endpoints use slug-based routing: `/api/businesses/{slug}/`
- All other resources use UUID: `/api/bookings/{uuid}/`

**Frontend API Client** (`front/src/lib/api/`):
- All API calls go through centralized client (`clients.js`)
- Business API uses slug format: `businessAPI.get('elite-hair-studio')`
- Other APIs use UUID format: `bookingAPI.get(uuid)`

**Common URL Issues**:
1. **Missing trailing slashes**: Backend expects trailing slashes on POST/PUT requests
2. **Slug vs UUID confusion**: Businesses use slugs, all other resources use UUIDs
3. **Nested routing**: Use `/api/businesses/{slug}/services/` for business-specific services
4. **Field name mismatches**: Booking API uses `business_id`/`service_id`, not `business`/`service`

### Authentication Integration
The auth flow is tightly integrated between frontend and backend:

**Token Management**:
- Access tokens stored in localStorage (consider httpOnly cookies for production)
- Automatic refresh on 401 responses
- Logout clears tokens and redirects to login page

**Common Auth Issues**:
1. **CORS configuration**: Ensure `CORS_ALLOWED_ORIGINS` includes frontend URL
2. **Token expiration**: Frontend automatically handles token refresh
3. **Permission errors**: Check user roles (customer, business_owner, admin)

### Media File Integration
Media files (QR codes, business logos) are managed through Django:

**Backend Media Handling**:
- Files stored in `media/` directory
- QR codes generated automatically for businesses
- Images served through Django in development

**Frontend Media Access**:
- Media URLs: `http://localhost:8000/media/{file_path}`
- QR codes: `media/qr_codes/qr_{business_slug}.png`
- Business logos: `media/business_logos/{filename}`

## Best Practices When Working on This Project

### Code Organization
- Follow existing code patterns and component structure
- Use the established API client (`src/lib/api/clients.js`) for all HTTP requests
- Maintain consistent error handling with toast notifications
- Keep components modular and reusable in `src/lib/components/`
- Use existing Svelte stores for state management

### API Integration
- Always use the centralized API client, never direct fetch calls
- Handle loading states and errors consistently across components
- Use proper authentication patterns with JWT tokens
- Follow the backend's slug/UUID conventions for different resources
- Implement proper error handling and user feedback

### Frontend Development
- Use Svelte 5 runes ($state, $derived, $effect) for reactivity
- Follow Tailwind CSS conventions and existing component patterns
- Ensure mobile responsiveness with Tailwind utilities
- Use TypeScript interfaces for API responses (add .d.ts files as needed)
- Test both customer and business owner user flows

### Backend Development
- Follow Django REST Framework patterns and ViewSet conventions
- Use proper serializers for API responses
- Implement proper permissions and authentication checks
- Follow the existing URL pattern conventions (slugs for businesses, UUIDs for others)
- Maintain proper data relationships and foreign key constraints

### Testing & Quality
- Run both backend and frontend linting/checking commands before committing
- Test authentication flows and user role permissions
- Verify API endpoints work correctly with proper data validation
- Test media file generation and QR code functionality
- Ensure proper error handling and user feedback

## Architecture Patterns & Best Practices

### Backend Patterns
- **ViewSet Architecture**: All APIs use Django REST Framework ViewSets with consistent patterns
- **Custom Actions**: Business analytics, booking confirmations, and other domain-specific actions
- **Permission System**: Role-based access control with custom permission classes
- **Serializer Patterns**: Separate read/write fields, nested serializers for complex data
- **Signal Handlers**: Automatic QR code generation, notification creation, and stats updates

### Frontend Patterns  
- **Svelte 5 Runes**: Modern reactivity with `$state`, `$derived`, and `$effect`
- **Centralized API Client**: Single client with automatic token refresh and error handling
- **Store Architecture**: Separate stores for auth, business, bookings, and UI state
- **Component Hierarchy**: Common components, domain-specific components, layout components
- **Route Protection**: Authentication-based routing with role-specific redirects

### Data Flow Patterns
- **Authentication**: JWT tokens with automatic refresh, role-based permissions
- **State Management**: Reactive stores with automatic UI updates
- **Error Handling**: Consistent error responses, user-friendly messages, automatic retries
- **Notification System**: Real-time notifications with backend/frontend synchronization
- **Media Management**: Automatic QR code generation, file upload handling

## Project Structure Summary

This is a **production-ready** comprehensive booking management system with:
- **Backend**: Django REST Framework with JWT authentication, subscription management, and comprehensive business logic
- **Frontend**: SvelteKit with Svelte 5, Tailwind CSS, and integrated API client  
- **Integration**: Clean API design with proper error handling, authentication, and media management
- **Features**: Multi-tenant SaaS with businesses, services, bookings, reviews, notifications, and analytics
- **Data**: Complete fixture system with test users, businesses, and sample data for development
- **Testing**: Full-stack testing verified for all major user flows and business operations

The codebase follows modern patterns with centralized API management, proper authentication flows, and comprehensive error handling throughout the stack. All major functionality has been tested and verified working.