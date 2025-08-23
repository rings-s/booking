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
        """
        Validate booking data and associate business and service instances
        """
        from django.shortcuts import get_object_or_404
        from django.core.exceptions import ValidationError
        from datetime import datetime, time
        
        # Get business and service instances from UUIDs
        business_id = attrs.get('business_id')
        service_id = attrs.get('service_id')
        
        if not business_id:
            raise serializers.ValidationError({'business_id': 'Business ID is required'})
        if not service_id:
            raise serializers.ValidationError({'service_id': 'Service ID is required'})
        
        try:
            business = Business.objects.get(id=business_id, is_active=True)
            attrs['business'] = business
        except Business.DoesNotExist:
            raise serializers.ValidationError({'business_id': 'Invalid or inactive business'})
        
        try:
            service = Service.objects.get(id=service_id, is_active=True)
            attrs['service'] = service
        except Service.DoesNotExist:
            raise serializers.ValidationError({'service_id': 'Invalid or inactive service'})
        
        # Validate service belongs to business
        if service.business != business:
            raise serializers.ValidationError({
                'service_id': 'Service does not belong to the specified business'
            })
        
        # Validate booking date and time
        booking_date = attrs.get('booking_date')
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')
        
        if not booking_date:
            raise serializers.ValidationError({'booking_date': 'Booking date is required'})
        if not start_time:
            raise serializers.ValidationError({'start_time': 'Start time is required'})
        if not end_time:
            raise serializers.ValidationError({'end_time': 'End time is required'})
        
        # Validate booking is not in the past
        from django.utils import timezone
        now = timezone.now()
        booking_datetime = datetime.combine(booking_date, start_time)
        
        if booking_datetime <= now:
            raise serializers.ValidationError({
                'booking_date': 'Cannot book appointments in the past'
            })
        
        # Validate end time is after start time
        if end_time <= start_time:
            raise serializers.ValidationError({
                'end_time': 'End time must be after start time'
            })
        
        # Calculate duration and validate against service duration
        duration_minutes = (datetime.combine(booking_date, end_time) - 
                          datetime.combine(booking_date, start_time)).total_seconds() / 60
        
        if abs(duration_minutes - service.duration_minutes) > 5:  # 5 minute tolerance
            raise serializers.ValidationError({
                'end_time': f'Booking duration must match service duration ({service.duration_minutes} minutes)'
            })
        
        # Validate business hours
        weekday = booking_date.weekday()
        business_hours = business.hours.filter(weekday=weekday, is_closed=False).first()
        
        if not business_hours:
            raise serializers.ValidationError({
                'booking_date': 'Business is closed on this day'
            })
        
        if start_time < business_hours.opening_time or end_time > business_hours.closing_time:
            raise serializers.ValidationError({
                'start_time': f'Booking must be within business hours ({business_hours.opening_time} - {business_hours.closing_time})'
            })
        
        # Check for booking conflicts (excluding current booking for updates)
        existing_bookings = Booking.objects.filter(
            business=business,
            booking_date=booking_date,
            status__in=['pending', 'confirmed']
        )
        
        # Exclude current booking if this is an update
        if self.instance:
            existing_bookings = existing_bookings.exclude(id=self.instance.id)
        
        for existing in existing_bookings:
            # Check for time overlap
            if (start_time < existing.end_time and end_time > existing.start_time):
                raise serializers.ValidationError({
                    'start_time': f'Time slot conflicts with existing booking ({existing.start_time} - {existing.end_time})'
                })
        
        # Check service capacity
        overlapping_bookings = existing_bookings.filter(
            service=service,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).count()
        
        if overlapping_bookings >= service.max_bookings_per_slot:
            raise serializers.ValidationError({
                'start_time': 'This time slot is fully booked for this service'
            })
        
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