#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append('/home/ahmed/tech-Savvy-projects/2025/new_ones/booking/back')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')

django.setup()

from django.contrib.auth import get_user_model
from accounts.models import SubscriptionPlan, Subscription
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def create_admin_user():
    email = 'admin@email.com'
    password = 'admin12345'
    first_name = 'Admin'
    last_name = 'User'

    # Check if user already exists
    if User.objects.filter(email=email).exists():
        print(f'User with email {email} already exists!')
        user = User.objects.get(email=email)
        print(f'User details: {user.email}, active: {user.is_active}')
        return user

    # Create user
    try:
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type='business_owner',  # Making admin a business owner
            email_verified=True,
            is_staff=True,  # Make staff user
            is_superuser=True  # Make superuser
        )

        # Create free subscription plan if it doesn't exist
        free_plan, created = SubscriptionPlan.objects.get_or_create(
            name='free',
            defaults={
                'price': 0.00,
                'max_businesses': 1,
                'max_services': 5,
                'max_bookings_per_month': 50,
                'analytics_enabled': False,
                'priority_support': False,
                'custom_branding': False,
                'api_access': False
            }
        )

        if created:
            print('Created free subscription plan')

        # Create subscription for user
        subscription = Subscription.objects.create(
            user=user,
            plan=free_plan,
            status='active',
            current_period_start=timezone.now(),
            current_period_end=timezone.now() + timedelta(days=30)
        )

        print(f'✅ Successfully created admin user: {email}')
        print(f'📧 Email: {email}')
        print(f'🔑 Password: {password}')
        print(f'👤 Name: {first_name} {last_name}')
        print(f'🏢 User Type: {user.user_type}')
        print(f'🔧 Staff: {user.is_staff}')
        print(f'⚡ Superuser: {user.is_superuser}')
        print(f'📋 Subscription: {subscription.plan.name}')
        print('✨ You can now test login with these credentials!')

        return user

    except Exception as e:
        print(f'❌ Error creating user: {str(e)}')
        return None

if __name__ == '__main__':
    create_admin_user()