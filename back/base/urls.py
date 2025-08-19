# base/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers as nested_routers
from .views import (
    BusinessViewSet,
    ServiceViewSet,
    BookingViewSet,
    CustomerViewSet,
    ReviewViewSet,
    NotificationViewSet,
    BusinessHoursViewSet
)

app_name = 'base'

# Main router
router = DefaultRouter()

# Register main viewsets
router.register(r'businesses', BusinessViewSet, basename='business')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'business-hours', BusinessHoursViewSet, basename='businesshours')

# Nested routers for related resources
businesses_router = nested_routers.NestedDefaultRouter(router, r'businesses', lookup='business')
businesses_router.register(r'services', ServiceViewSet, basename='business-services')
businesses_router.register(r'reviews', ReviewViewSet, basename='business-reviews')
businesses_router.register(r'bookings', BookingViewSet, basename='business-bookings')
businesses_router.register(r'hours', BusinessHoursViewSet, basename='business-hours')

# URL patterns
urlpatterns = [
    # Custom endpoints MUST come before router URLs to avoid conflicts
    
    # Custom notification endpoints
    path('notifications/unread-count/', 
         NotificationViewSet.as_view({'get': 'unread_count'}), 
         name='notification-unread-count'),
    
    path('notifications/mark-all-read/', 
         NotificationViewSet.as_view({'post': 'mark_all_read'}), 
         name='notification-mark-all-read'),
    
    path('notifications/<uuid:pk>/mark-read/', 
         NotificationViewSet.as_view({'post': 'mark_read'}), 
         name='notification-mark-read'),
    
    path('notifications/clear-all/', 
         NotificationViewSet.as_view({'delete': 'clear_all'}), 
         name='notification-clear-all'),
    
    # Custom booking endpoints
    path('bookings/chart-data/', 
         BookingViewSet.as_view({'get': 'chart_data'}), 
         name='booking-chart-data'),
    
    path('bookings/upcoming/', 
         BookingViewSet.as_view({'get': 'upcoming'}), 
         name='booking-upcoming'),
    
    path('bookings/history/', 
         BookingViewSet.as_view({'get': 'history'}), 
         name='booking-history'),
    
    path('bookings/<uuid:pk>/confirm/', 
         BookingViewSet.as_view({'post': 'confirm'}), 
         name='booking-confirm'),
    
    path('bookings/<uuid:pk>/cancel/', 
         BookingViewSet.as_view({'post': 'cancel'}), 
         name='booking-cancel'),
    
    path('bookings/<uuid:pk>/complete/', 
         BookingViewSet.as_view({'post': 'complete'}), 
         name='booking-complete'),
    
    path('bookings/<uuid:pk>/mark-no-show/', 
         BookingViewSet.as_view({'post': 'mark_no_show'}), 
         name='booking-mark-no-show'),
    
    # Custom business endpoints
    path('businesses/search/', 
         BusinessViewSet.as_view({'get': 'search'}), 
         name='business-search'),
    
    path('businesses/featured/', 
         BusinessViewSet.as_view({'get': 'featured'}), 
         name='business-featured'),
    
    path('businesses/my/', 
         BusinessViewSet.as_view({'get': 'my'}), 
         name='business-my'),
    
    path('businesses/<slug:slug>/dashboard/', 
         BusinessViewSet.as_view({'get': 'dashboard'}), 
         name='business-dashboard'),
    
    path('businesses/<slug:slug>/analytics-chart/', 
         BusinessViewSet.as_view({'get': 'analytics_chart'}), 
         name='business-analytics-chart'),
    
    path('businesses/<slug:slug>/available-slots/', 
         BusinessViewSet.as_view({'get': 'available_slots'}), 
         name='business-available-slots'),
    
    path('businesses/<slug:slug>/available-dates/', 
         BusinessViewSet.as_view({'get': 'available_dates'}), 
         name='business-available-dates'),
    
    path('businesses/<slug:slug>/update-hours/', 
         BusinessViewSet.as_view({'post': 'update_hours'}), 
         name='business-update-hours'),
    
    path('businesses/<slug:slug>/revenue-report/', 
         BusinessViewSet.as_view({'get': 'revenue_report'}), 
         name='business-revenue-report'),
    
    path('businesses/<slug:slug>/stats/', 
         BusinessViewSet.as_view({'get': 'stats'}), 
         name='business-stats'),
    
    path('businesses/<slug:slug>/revenue-data/', 
         BusinessViewSet.as_view({'get': 'revenue_data'}), 
         name='business-revenue-data'),
    
    path('businesses/<slug:slug>/service-stats/', 
         BusinessViewSet.as_view({'get': 'service_stats'}), 
         name='business-service-stats'),
    
    path('businesses/<slug:slug>/recent-activity/', 
         BusinessViewSet.as_view({'get': 'recent_activity'}), 
         name='business-recent-activity'),
    
    # Custom service endpoints
    path('services/bulk-update/', 
         ServiceViewSet.as_view({'post': 'bulk_update'}), 
         name='service-bulk-update'),
    
    path('services/update-order/', 
         ServiceViewSet.as_view({'post': 'update_order'}), 
         name='service-update-order'),
    
    # Custom customer endpoints
    path('customers/me/', 
         CustomerViewSet.as_view({'get': 'me'}), 
         name='customer-me'),
    
    path('customers/analytics/', 
         CustomerViewSet.as_view({'get': 'analytics'}), 
         name='customer-analytics'),
    
    path('customers/me/add-preferred-business/', 
         CustomerViewSet.as_view({'post': 'add_preferred_business_me'}), 
         name='customer-add-preferred-me'),
    
    path('customers/<uuid:pk>/add-preferred-business/', 
         CustomerViewSet.as_view({'post': 'add_preferred_business'}), 
         name='customer-add-preferred'),
    
    path('customers/<uuid:pk>/remove-preferred-business/', 
         CustomerViewSet.as_view({'post': 'remove_preferred_business'}), 
         name='customer-remove-preferred'),
    
    path('customers/<uuid:pk>/booking-history/', 
         CustomerViewSet.as_view({'get': 'booking_history'}), 
         name='customer-booking-history'),
    
    path('customers/<uuid:pk>/stats/', 
         CustomerViewSet.as_view({'get': 'stats'}), 
         name='customer-stats'),
    
    # Custom review endpoints
    path('reviews/<uuid:pk>/respond/', 
         ReviewViewSet.as_view({'post': 'respond'}), 
         name='review-respond'),
    
    path('reviews/<uuid:pk>/mark-featured/', 
         ReviewViewSet.as_view({'post': 'mark_featured'}), 
         name='review-mark-featured'),
    
    # Main router URLs
    path('', include(router.urls)),
    
    # Nested router URLs
    path('', include(businesses_router.urls)),
]

# Alternative simpler version without nested routers
# If you don't want to use drf-nested-routers, use this instead:

"""
# base/urls.py (Alternative without nested routers)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BusinessViewSet,
    ServiceViewSet,
    BookingViewSet,
    CustomerViewSet,
    ReviewViewSet,
    NotificationViewSet,
    BusinessHoursViewSet
)

app_name = 'base'

router = DefaultRouter()

# Register viewsets
router.register(r'businesses', BusinessViewSet, basename='business')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'business-hours', BusinessHoursViewSet, basename='businesshours')

urlpatterns = [
    path('', include(router.urls)),
]
"""