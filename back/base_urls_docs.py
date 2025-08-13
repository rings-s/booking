# base/urls_documentation.py
"""
API Endpoints Documentation for Base App

Business Endpoints:
==================
GET     /api/businesses/                      - List all businesses
POST    /api/businesses/                      - Create a new business
GET     /api/businesses/{slug}/               - Get business details
PUT     /api/businesses/{slug}/               - Update business
PATCH   /api/businesses/{slug}/               - Partial update business
DELETE  /api/businesses/{slug}/               - Delete business

Business Custom Actions:
GET     /api/businesses/{slug}/dashboard/     - Get business dashboard data
GET     /api/businesses/{slug}/analytics-chart/ - Get analytics charts
        Query params: type (bookings/revenue/services/customers/heatmap), period (days)
GET     /api/businesses/{slug}/available-slots/ - Get available booking slots
        Query params: service (UUID), date (YYYY-MM-DD)
POST    /api/businesses/{slug}/update-hours/  - Update business hours
GET     /api/businesses/{slug}/revenue-report/ - Get revenue report
        Query params: period (week/month/quarter/year)

Service Endpoints:
==================
GET     /api/services/                        - List all services
        Query params: business, min_price, max_price
POST    /api/services/                        - Create a new service
GET     /api/services/{id}/                   - Get service details
PUT     /api/services/{id}/                   - Update service
PATCH   /api/services/{id}/                   - Partial update service
DELETE  /api/services/{id}/                   - Delete service

Booking Endpoints:
==================
GET     /api/bookings/                        - List bookings (filtered by user type)
        Query params: status, business, service, booking_date, start_date, end_date
POST    /api/bookings/                        - Create a new booking
GET     /api/bookings/{id}/                   - Get booking details
PUT     /api/bookings/{id}/                   - Update booking
PATCH   /api/bookings/{id}/                   - Partial update booking
DELETE  /api/bookings/{id}/                   - Delete booking

Booking Custom Actions:
POST    /api/bookings/{id}/confirm/          - Confirm a pending booking
POST    /api/bookings/{id}/cancel/           - Cancel a booking
POST    /api/bookings/{id}/complete/         - Mark booking as completed
POST    /api/bookings/{id}/mark-no-show/     - Mark booking as no-show
GET     /api/bookings/upcoming/              - Get upcoming bookings
GET     /api/bookings/history/               - Get booking history

Customer Endpoints:
===================
GET     /api/customers/                       - List customers
POST    /api/customers/                       - Create customer profile
GET     /api/customers/{id}/                  - Get customer details
PUT     /api/customers/{id}/                  - Update customer
PATCH   /api/customers/{id}/                  - Partial update customer
DELETE  /api/customers/{id}/                  - Delete customer

Customer Custom Actions:
GET     /api/customers/me/                    - Get current user's customer profile
POST    /api/customers/{id}/add-preferred-business/ - Add business to favorites

Review Endpoints:
=================
GET     /api/reviews/                         - List reviews
        Query params: business, rating, min_rating
POST    /api/reviews/                         - Create a new review
GET     /api/reviews/{id}/                    - Get review details
PUT     /api/reviews/{id}/                    - Update review
PATCH   /api/reviews/{id}/                    - Partial update review
DELETE  /api/reviews/{id}/                    - Delete review

Review Custom Actions:
POST    /api/reviews/{id}/respond/           - Business owner responds to review
POST    /api/reviews/{id}/mark-featured/     - Mark review as featured

Notification Endpoints:
=======================
GET     /api/notifications/                    - List user's notifications
        Query params: type, is_read
POST    /api/notifications/                    - Create notification (admin only)
GET     /api/notifications/{id}/               - Get notification details
PUT     /api/notifications/{id}/               - Update notification
PATCH   /api/notifications/{id}/               - Partial update notification
DELETE  /api/notifications/{id}/               - Delete notification

Notification Custom Actions:
POST    /api/notifications/{id}/mark-read/    - Mark notification as read
POST    /api/notifications/mark-all-read/    - Mark all notifications as read
GET     /api/notifications/unread-count/     - Get count of unread notifications
DELETE  /api/notifications/clear-all/        - Clear all read notifications

Business Hours Endpoints:
=========================
GET     /api/business-hours/                  - List business hours
        Query params: business
POST    /api/business-hours/                  - Create business hours
GET     /api/business-hours/{id}/             - Get business hours details
PUT     /api/business-hours/{id}/             - Update business hours
PATCH   /api/business-hours/{id}/             - Partial update business hours
DELETE  /api/business-hours/{id}/             - Delete business hours

Nested Endpoints (if using nested routers):
============================================
GET     /api/businesses/{slug}/services/      - List services for a business
POST    /api/businesses/{slug}/services/      - Add service to business
GET     /api/businesses/{slug}/reviews/       - List reviews for a business
GET     /api/businesses/{slug}/bookings/      - List bookings for a business
GET     /api/businesses/{slug}/hours/         - List business hours

Authentication Required:
========================
Most endpoints require authentication via JWT token in headers:
Authorization: Bearer <access_token>

Public Endpoints (No authentication required):
==============================================
- GET /api/businesses/
- GET /api/businesses/{slug}/
- GET /api/businesses/{slug}/available-slots/
- GET /api/services/
- GET /api/services/{id}/
- GET /api/reviews/
- GET /api/reviews/{id}/
- GET /api/business-hours/

Permissions:
============
- Business owners can only modify their own businesses
- Customers can only modify their own profiles and bookings
- Reviews can only be created by customers who have completed bookings
- Notifications are user-specific
"""