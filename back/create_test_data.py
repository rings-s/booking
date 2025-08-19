#!/usr/bin/env python
"""
Create test data for the booking management system
"""
import os
import sys
import django
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')
django.setup()

from django.contrib.auth import get_user_model
from base.models import Business, Customer, Service, Booking, Review
from accounts.models import Subscription

User = get_user_model()

def create_test_data():
    print("Creating test data...")
    
    # Create business owner user
    business_owner, created = User.objects.get_or_create(
        email='john.doe@example.com',
        defaults={
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': 'business_owner',
            'is_active': True
        }
    )
    if created:
        business_owner.set_password('password')
        business_owner.save()
        print(f"Created business owner: {business_owner.email}")
    
    # Create customer users
    customers = []
    customer_data = [
        ('mike.wilson@example.com', 'Mike Wilson'),
        ('sarah.jones@example.com', 'Sarah Jones'),
        ('david.brown@example.com', 'David Brown'),
        ('lisa.davis@example.com', 'Lisa Davis'),
        ('tom.miller@example.com', 'Tom Miller'),
    ]
    
    for email, name in customer_data:
        first_name, last_name = name.split(' ', 1)
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'user_type': 'customer',
                'is_active': True
            }
        )
        if created:
            user.set_password('password')
            user.save()
            print(f"Created customer user: {user.email}")
        
        # Create customer profile
        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={
                'phone': f'+1-555-{len(customers) + 1000:04d}',
                'receive_notifications': True,
                'total_bookings': 0,
                'total_spent': Decimal('0.00')
            }
        )
        customers.append(customer)
    
    # Create business
    business, created = Business.objects.get_or_create(
        slug='elite-hair-studio',
        defaults={
            'owner': business_owner,
            'name': 'Elite Hair Studio',
            'description': 'Premium hair salon offering cutting-edge styles and treatments',
            'email': 'info@elitehairstudio.com',
            'phone': '+1-555-0123',
            'website': 'https://elitehairstudio.com',
            'address': '123 Main Street',
            'city': 'New York',
            'state': 'NY',
            'country': 'USA',
            'postal_code': '10001',
            'category': 'Beauty & Wellness',
            'is_active': True,
            'accepts_online_bookings': True,
            'auto_confirm_bookings': False
        }
    )
    if created:
        print(f"Created business: {business.name}")
    
    # Create services
    services_data = [
        ('Hair Cut & Style', 'Professional haircut with styling', 60, '75.00'),
        ('Hair Color', 'Full hair coloring service', 120, '150.00'),
        ('Hair Wash & Blowdry', 'Shampoo, condition and blowdry', 45, '45.00'),
        ('Highlights', 'Professional hair highlighting', 90, '120.00'),
        ('Deep Conditioning', 'Intensive hair treatment', 30, '35.00'),
        ('Bridal Package', 'Complete bridal hair and makeup', 180, '300.00'),
    ]
    
    services = []
    for name, desc, duration, price in services_data:
        service, created = Service.objects.get_or_create(
            business=business,
            name=name,
            defaults={
                'description': desc,
                'duration_minutes': duration,
                'price': Decimal(price),
                'is_active': True,
                'max_bookings_per_slot': 1,
                'buffer_time_minutes': 15
            }
        )
        services.append(service)
        if created:
            print(f"Created service: {service.name}")
    
    # Create bookings for the last 90 days
    print("Creating bookings...")
    start_date = date.today() - timedelta(days=90)
    end_date = date.today() + timedelta(days=30)
    
    booking_count = 0
    current_date = start_date
    
    while current_date <= end_date:
        # Skip some days randomly to make it realistic
        if current_date.weekday() in [0, 1, 2, 3, 4]:  # Weekdays
            num_bookings = 3 if current_date < date.today() else 2  # Fewer future bookings
        else:  # Weekends
            num_bookings = 5 if current_date < date.today() else 3
        
        for i in range(num_bookings):
            # Pick random customer and service
            customer = customers[i % len(customers)]
            service = services[i % len(services)]
            
            # Create booking time
            hour = 9 + (i * 2)  # Spread throughout day
            start_time = datetime.combine(current_date, datetime.min.time().replace(hour=hour))
            end_time = start_time + timedelta(minutes=service.duration_minutes)
            
            # Determine status based on date
            if current_date < date.today():
                status = 'completed' if i % 5 != 0 else 'cancelled'
            elif current_date == date.today():
                status = 'confirmed'
            else:
                status = 'pending'
            
            booking, created = Booking.objects.get_or_create(
                business=business,
                customer=customer,
                service=service,
                booking_date=current_date,
                start_time=start_time.time(),
                defaults={
                    'end_time': end_time.time(),
                    'status': status,
                    'total_price': service.price,
                    'is_paid': status == 'completed',
                    'payment_method': 'card' if status == 'completed' else '',
                    'notes': f'Booking #{booking_count + 1}'
                }
            )
            
            if created:
                booking_count += 1
                # Update customer stats
                if status == 'completed':
                    customer.total_bookings += 1
                    customer.total_spent += service.price
                    customer.save()
        
        current_date += timedelta(days=1)
    
    print(f"Created {booking_count} bookings")
    
    # Create reviews for completed bookings
    print("Creating reviews...")
    completed_bookings = Booking.objects.filter(status='completed')
    review_count = 0
    
    for booking in completed_bookings[:20]:  # Create reviews for first 20 completed bookings
        rating = 4 if review_count % 5 == 0 else 5  # Mostly 5-star reviews
        
        review_texts = [
            "Excellent service! Very professional staff.",
            "Amazing results, couldn't be happier!",
            "Great experience, will definitely come back.",
            "Professional and friendly service.",
            "Love my new look! Highly recommend.",
            "Outstanding quality and attention to detail.",
            "Perfect styling, exactly what I wanted.",
            "Great atmosphere and skilled stylists.",
            "Exceeded my expectations in every way.",
            "Beautiful results and wonderful experience."
        ]
        
        review, created = Review.objects.get_or_create(
            business=business,
            customer=booking.customer,
            booking=booking,
            defaults={
                'rating': rating,
                'title': f'Great experience at {business.name}',
                'comment': review_texts[review_count % len(review_texts)],
                'is_verified': True,
                'is_featured': rating == 5 and review_count % 3 == 0
            }
        )
        
        if created:
            review_count += 1
    
    print(f"Created {review_count} reviews")
    
    print("\nTest data creation completed!")
    print(f"Login credentials:")
    print(f"Business Owner: john.doe@example.com / password")
    print(f"Customer: mike.wilson@example.com / password")
    print(f"Business: {business.name} (slug: {business.slug})")
    print(f"Frontend: http://localhost:5174/dashboard")
    print(f"Backend: http://localhost:8001/api/businesses/{business.slug}/dashboard/")

if __name__ == '__main__':
    create_test_data()