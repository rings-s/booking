# base/serializers.py
from rest_framework import serializers
from .models import (
    Business, BusinessHours, Service, Customer, 
    Booking, Review, Notification
)
from accounts.serializers import UserSerializer

class BusinessHoursSerializer(serializers.ModelSerializer):
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    
    class Meta:
        model = BusinessHours
        fields = ['id', 'weekday', 'weekday_display', 'opening_time', 
                 'closing_time', 'is_closed']


class ServiceSerializer(serializers.ModelSerializer):
    business = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Service
        fields = ['id', 'business', 'name', 'description', 'duration_minutes', 
                 'price', 'is_active', 'max_bookings_per_slot', 
                 'buffer_time_minutes', 'created_at']
        read_only_fields = ['id', 'created_at']


class BusinessSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    hours = BusinessHoursSerializer(many=True, read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = ['id', 'owner', 'name', 'slug', 'description', 'email', 
                 'phone', 'website', 'address', 'city', 'state', 'country', 
                 'postal_code', 'category', 'logo', 'cover_image', 'qr_code',
                 'is_active', 'accepts_online_bookings', 'auto_confirm_bookings',
                 'hours', 'services', 'average_rating', 'total_reviews',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'owner', 'qr_code', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(r.rating for r in reviews) / len(reviews), 1)
        return 0
    
    def get_total_reviews(self, obj):
        return obj.reviews.count()


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    preferred_businesses = BusinessSerializer(many=True, read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'date_of_birth', 
                 'preferred_businesses', 'receive_notifications',
                 'receive_marketing_emails', 'total_bookings', 
                 'total_spent', 'created_at']
        read_only_fields = ['id', 'user', 'total_bookings', 'total_spent', 'created_at']


class BookingSerializer(serializers.ModelSerializer):
    business = BusinessSerializer(read_only=True)
    business_id = serializers.UUIDField(write_only=True)
    customer = CustomerSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    service_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'business', 'business_id', 'customer', 'service', 
                 'service_id', 'booking_date', 'start_time', 'end_time', 
                 'status', 'notes', 'total_price', 'is_paid', 'payment_method',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'customer', 'total_price', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        # Validate booking time is within business hours
        # Validate no conflicts with existing bookings
        # Implementation would go here
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    business = BusinessSerializer(read_only=True)
    business_id = serializers.UUIDField(write_only=True)
    booking_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Review
        fields = ['id', 'business', 'business_id', 'customer', 'booking_id',
                 'rating', 'title', 'comment', 'is_verified', 'is_featured',
                 'business_response', 'response_date', 'created_at']
        read_only_fields = ['id', 'customer', 'is_verified', 'is_featured', 
                          'business_response', 'response_date', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    booking = BookingSerializer(read_only=True)
    business = BusinessSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'type', 'title', 'message', 'booking', 
                 'business', 'is_read', 'read_at', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class DashboardSerializer(serializers.Serializer):
    """Serializer for dashboard analytics data"""
    total_bookings = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_customers = serializers.IntegerField()
    average_rating = serializers.FloatField()
    
    # Time series data for charts
    bookings_by_date = serializers.ListField(child=serializers.DictField())
    revenue_by_month = serializers.ListField(child=serializers.DictField())
    popular_services = serializers.ListField(child=serializers.DictField())
    customer_demographics = serializers.DictField()