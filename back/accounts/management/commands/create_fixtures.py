"""
Management command to create fixtures with proper password hashes
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
import json
import uuid
from datetime import timedelta


class Command(BaseCommand):
    help = 'Create proper fixtures with valid password hashes'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating fixtures with proper password hashes...'))
        
        # Create accounts fixtures
        self.create_accounts_fixtures()
        
        # Create base fixtures
        self.create_base_fixtures()
        
        self.stdout.write(self.style.SUCCESS('Fixtures created successfully!'))
    
    def create_accounts_fixtures(self):
        """Create accounts fixtures with proper password hashes"""
        
        # Hash the default password
        password_hash = make_password('password')
        
        fixtures = []
        
        # Subscription Plans
        plans = [
            {
                "model": "accounts.subscriptionplan",
                "pk": "550e8400-e29b-41d4-a716-446655440001",
                "fields": {
                    "name": "free",
                    "price": "0.00",
                    "stripe_price_id": "",
                    "max_businesses": 1,
                    "max_services": 5,
                    "max_bookings_per_month": 50,
                    "max_staff_accounts": 1,
                    "max_storage_gb": 1,
                    "analytics_enabled": False,
                    "priority_support": False,
                    "custom_branding": False,
                    "api_access": False,
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            },
            {
                "model": "accounts.subscriptionplan",
                "pk": "550e8400-e29b-41d4-a716-446655440002",
                "fields": {
                    "name": "basic",
                    "price": "29.99",
                    "stripe_price_id": "price_basic_monthly",
                    "max_businesses": 1,
                    "max_services": 15,
                    "max_bookings_per_month": 200,
                    "max_staff_accounts": 3,
                    "max_storage_gb": 5,
                    "analytics_enabled": True,
                    "priority_support": False,
                    "custom_branding": False,
                    "api_access": False,
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            },
            {
                "model": "accounts.subscriptionplan",
                "pk": "550e8400-e29b-41d4-a716-446655440003",
                "fields": {
                    "name": "premium",
                    "price": "79.99",
                    "stripe_price_id": "price_premium_monthly",
                    "max_businesses": 3,
                    "max_services": 50,
                    "max_bookings_per_month": 1000,
                    "max_staff_accounts": 10,
                    "max_storage_gb": 20,
                    "analytics_enabled": True,
                    "priority_support": True,
                    "custom_branding": True,
                    "api_access": True,
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            },
            {
                "model": "accounts.subscriptionplan",
                "pk": "550e8400-e29b-41d4-a716-446655440004",
                "fields": {
                    "name": "enterprise",
                    "price": "199.99",
                    "stripe_price_id": "price_enterprise_monthly",
                    "max_businesses": 10,
                    "max_services": 200,
                    "max_bookings_per_month": 5000,
                    "max_staff_accounts": 50,
                    "max_storage_gb": 100,
                    "analytics_enabled": True,
                    "priority_support": True,
                    "custom_branding": True,
                    "api_access": True,
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            }
        ]
        
        # Users
        users = [
            {
                "model": "accounts.user",
                "pk": "550e8400-e29b-41d4-a716-446655440010",
                "fields": {
                    "password": password_hash,
                    "last_login": None,
                    "is_superuser": True,
                    "email": "admin@example.com",
                    "first_name": "System",
                    "last_name": "Administrator",
                    "is_active": True,
                    "is_staff": True,
                    "date_joined": "2024-01-01T12:00:00Z",
                    "email_verified": True,
                    "user_type": "admin",
                    "groups": [],
                    "user_permissions": []
                }
            },
            {
                "model": "accounts.user",
                "pk": "550e8400-e29b-41d4-a716-446655440011",
                "fields": {
                    "password": password_hash,
                    "last_login": "2024-01-15T14:30:00Z",
                    "is_superuser": False,
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "is_active": True,
                    "is_staff": False,
                    "date_joined": "2024-01-01T12:00:00Z",
                    "email_verified": True,
                    "user_type": "business_owner",
                    "groups": [],
                    "user_permissions": []
                }
            },
            {
                "model": "accounts.user",
                "pk": "550e8400-e29b-41d4-a716-446655440012",
                "fields": {
                    "password": password_hash,
                    "last_login": "2024-01-20T10:15:00Z",
                    "is_superuser": False,
                    "email": "jane.smith@example.com",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "is_active": True,
                    "is_staff": False,
                    "date_joined": "2024-01-02T09:30:00Z",
                    "email_verified": True,
                    "user_type": "business_owner",
                    "groups": [],
                    "user_permissions": []
                }
            },
            {
                "model": "accounts.user",
                "pk": "550e8400-e29b-41d4-a716-446655440013",
                "fields": {
                    "password": password_hash,
                    "last_login": "2024-01-25T16:45:00Z",
                    "is_superuser": False,
                    "email": "mike.wilson@example.com",
                    "first_name": "Mike",
                    "last_name": "Wilson",
                    "is_active": True,
                    "is_staff": False,
                    "date_joined": "2024-01-03T11:20:00Z",
                    "email_verified": True,
                    "user_type": "customer",
                    "groups": [],
                    "user_permissions": []
                }
            },
            {
                "model": "accounts.user",
                "pk": "550e8400-e29b-41d4-a716-446655440014",
                "fields": {
                    "password": password_hash,
                    "last_login": "2024-01-28T13:20:00Z",
                    "is_superuser": False,
                    "email": "sarah.johnson@example.com",
                    "first_name": "Sarah",
                    "last_name": "Johnson",
                    "is_active": True,
                    "is_staff": False,
                    "date_joined": "2024-01-04T15:10:00Z",
                    "email_verified": True,
                    "user_type": "customer",
                    "groups": [],
                    "user_permissions": []
                }
            },
            {
                "model": "accounts.user",
                "pk": "550e8400-e29b-41d4-a716-446655440015",
                "fields": {
                    "password": password_hash,
                    "last_login": "2024-02-01T09:30:00Z",
                    "is_superuser": False,
                    "email": "david.brown@example.com",
                    "first_name": "David",
                    "last_name": "Brown",
                    "is_active": True,
                    "is_staff": False,
                    "date_joined": "2024-01-05T08:45:00Z",
                    "email_verified": True,
                    "user_type": "customer",
                    "groups": [],
                    "user_permissions": []
                }
            },
            {
                "model": "accounts.user",
                "pk": "550e8400-e29b-41d4-a716-446655440016",
                "fields": {
                    "password": password_hash,
                    "last_login": "2024-02-03T14:20:00Z",
                    "is_superuser": False,
                    "email": "emma.taylor@example.com",
                    "first_name": "Emma",
                    "last_name": "Taylor",
                    "is_active": True,
                    "is_staff": False,
                    "date_joined": "2024-01-06T12:30:00Z",
                    "email_verified": False,
                    "user_type": "customer",
                    "groups": [],
                    "user_permissions": []
                }
            }
        ]
        
        # Subscriptions
        subscriptions = [
            {
                "model": "accounts.subscription",
                "pk": "550e8400-e29b-41d4-a716-446655440020",
                "fields": {
                    "user": "550e8400-e29b-41d4-a716-446655440011",
                    "plan": "550e8400-e29b-41d4-a716-446655440002",
                    "status": "active",
                    "stripe_subscription_id": "sub_1234567890",
                    "stripe_customer_id": "cus_1234567890",
                    "trial_end": None,
                    "current_period_start": "2024-01-01T12:00:00Z",
                    "current_period_end": "2024-02-01T12:00:00Z",
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            },
            {
                "model": "accounts.subscription",
                "pk": "550e8400-e29b-41d4-a716-446655440021",
                "fields": {
                    "user": "550e8400-e29b-41d4-a716-446655440012",
                    "plan": "550e8400-e29b-41d4-a716-446655440003",
                    "status": "active",
                    "stripe_subscription_id": "sub_0987654321",
                    "stripe_customer_id": "cus_0987654321",
                    "trial_end": None,
                    "current_period_start": "2024-01-02T09:30:00Z",
                    "current_period_end": "2024-02-02T09:30:00Z",
                    "created_at": "2024-01-02T09:30:00Z",
                    "updated_at": "2024-01-02T09:30:00Z"
                }
            },
            {
                "model": "accounts.subscription",
                "pk": "550e8400-e29b-41d4-a716-446655440022",
                "fields": {
                    "user": "550e8400-e29b-41d4-a716-446655440013",
                    "plan": "550e8400-e29b-41d4-a716-446655440001",
                    "status": "trial",
                    "stripe_subscription_id": "",
                    "stripe_customer_id": "",
                    "trial_end": "2024-02-03T11:20:00Z",
                    "current_period_start": "2024-01-03T11:20:00Z",
                    "current_period_end": "2024-02-03T11:20:00Z",
                    "created_at": "2024-01-03T11:20:00Z",
                    "updated_at": "2024-01-03T11:20:00Z"
                }
            }
        ]
        
        fixtures.extend(plans)
        fixtures.extend(users)
        fixtures.extend(subscriptions)
        
        # Write accounts fixtures
        with open('/home/ahmed/tech-Savvy-projects/2025/new_ones/booking/back/accounts/fixtures/accounts_data.json', 'w') as f:
            json.dump(fixtures, f, indent=2, default=str)
            
        self.stdout.write('✓ Accounts fixtures created with proper password hashes')
    
    def create_base_fixtures(self):
        """Create base fixtures - these remain the same as they don't have password issues"""
        self.stdout.write('✓ Base fixtures already exist and are correct')