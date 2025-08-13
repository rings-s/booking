# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack booking management system built with Django REST Framework (backend) and SvelteKit (frontend). It allows businesses to manage services, bookings, customers, and provides features like payment integration, notifications, and analytics.

**Key Features:**
- Multi-tenant business management
- Service booking system with calendar integration
- Customer management and profiles
- Payment processing with Stripe
- Review and rating system
- Subscription-based SaaS model
- Real-time notifications
- Analytics dashboard
- QR code generation for businesses

## Development Commands

### Backend (Django)
```bash
cd back/
python manage.py runserver                    # Start development server (port 8000)
python manage.py migrate                      # Run database migrations
python manage.py makemigrations               # Create new migrations
python manage.py createsuperuser              # Create admin user
python manage.py collectstatic                # Collect static files
python manage.py shell                        # Django shell
python manage.py test                         # Run tests
python manage.py loaddata fixtures/data.json  # Load seed data
python scripts/seed_base.py                   # Run custom seed script
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
  - RESTful API with ViewSets
  - JWT authentication with refresh tokens
  - Nested routes for related resources (e.g., `/api/businesses/{slug}/services/`)
  - Custom actions for business operations (dashboard, analytics, available slots)

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

## Known Issues & Considerations

### Missing Components:
- **Frontend Routes:** Some routes referenced in navigation don't have corresponding page files:
  - `/features/*` - Referenced in homepage feature links
  - `/reviews/new` - Referenced in booking actions
  - Reviews section not fully implemented in businesses route structure

### Environment Dependencies:
- Backend requires Redis for Celery (background tasks)
- PostgreSQL configuration available but SQLite used by default
- Google OAuth requires proper client credentials
- Stripe integration requires test keys for development

### Security Considerations:
- CSRF protection enabled in Django
- JWT tokens stored in localStorage (consider httpOnly cookies for production)
- File uploads need proper validation
- CORS configuration should be restricted in production

### Performance Notes:
- Database uses SQLite by default (switch to PostgreSQL for production)
- No caching layer implemented yet
- Image uploads stored locally (consider cloud storage for production)
- No CDN configuration for static assets

### Development Workflow:
1. Start backend server first (Django on port 8000)
2. Start frontend development server (SvelteKit on port 5173)
3. Ensure Redis is running if testing background tasks
4. Run migrations before starting development
5. Create superuser for admin access

### Testing:
- Backend has test structure but needs test implementation
- Frontend uses Playwright for E2E testing
- No unit tests implemented yet for either frontend or backend

## Best Practices When Working on This Project:
- Follow existing code patterns and component structure
- Use the established API client for all HTTP requests
- Maintain consistent error handling with toast notifications
- Follow the existing authentication patterns
- Keep components modular and reusable
- Use TypeScript interfaces for API responses (add .d.ts files)
- Test both customer and business owner user flows
- Ensure mobile responsiveness with Tailwind utilities