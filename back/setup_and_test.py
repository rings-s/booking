#!/usr/bin/env python
"""
Complete setup and test script for the Django booking system
"""
import os
import sys
import django
from pathlib import Path

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')

# Setup Django
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from base.models import Business, Service, Customer, Booking
from accounts.models import SubscriptionPlan, Subscription
from django.db import connection

User = get_user_model()

def setup_database():
    """Setup database with migrations"""
    print("🔄 Setting up database...")
    try:
        call_command('migrate', verbosity=1, interactive=False)
        print("✅ Database migrations completed")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_fixtures():
    """Create fixtures with proper data"""
    print("🔄 Creating fixtures with proper password hashes...")
    try:
        call_command('create_fixtures')
        print("✅ Fixtures created successfully")
        return True
    except Exception as e:
        print(f"❌ Fixture creation failed: {e}")
        return False

def load_fixtures():
    """Load fixtures into database"""
    print("🔄 Loading fixtures...")
    try:
        # Load accounts fixtures first
        call_command('loaddata', 'accounts/fixtures/accounts_data.json', verbosity=1)
        print("✅ Accounts fixtures loaded")
        
        # Load base fixtures
        call_command('loaddata', 'base/fixtures/base_data.json', verbosity=1)
        print("✅ Base fixtures loaded")
        
        return True
    except Exception as e:
        print(f"❌ Fixture loading failed: {e}")
        return False

def test_data():
    """Test that data was loaded correctly"""
    print("🔄 Testing loaded data...")
    
    try:
        # Test users
        user_count = User.objects.count()
        admin_count = User.objects.filter(is_superuser=True).count()
        business_owner_count = User.objects.filter(user_type='business_owner').count()
        customer_count = User.objects.filter(user_type='customer').count()
        
        print(f"📊 Users: {user_count} total ({admin_count} admin, {business_owner_count} business owners, {customer_count} customers)")
        
        # Test subscription plans
        plan_count = SubscriptionPlan.objects.count()
        subscription_count = Subscription.objects.count()
        print(f"📊 Subscription Plans: {plan_count}, Active Subscriptions: {subscription_count}")
        
        # Test businesses
        business_count = Business.objects.count()
        service_count = Service.objects.count()
        print(f"📊 Businesses: {business_count}, Services: {service_count}")
        
        # Test bookings and customers
        customer_profile_count = Customer.objects.count()
        booking_count = Booking.objects.count()
        print(f"📊 Customer Profiles: {customer_profile_count}, Bookings: {booking_count}")
        
        # Test password authentication
        admin_user = User.objects.filter(email='admin@example.com').first()
        if admin_user and admin_user.check_password('password'):
            print("✅ Admin password authentication works")
        else:
            print("❌ Admin password authentication failed")
            
        business_user = User.objects.filter(email='john.doe@example.com').first()
        if business_user and business_user.check_password('password'):
            print("✅ Business owner password authentication works")
        else:
            print("❌ Business owner password authentication failed")
            
        return True
        
    except Exception as e:
        print(f"❌ Data testing failed: {e}")
        return False

def test_media():
    """Test media and QR code generation"""
    print("🔄 Testing media and QR code generation...")
    try:
        call_command('test_media_qr')
        print("✅ Media and QR code tests completed")
        return True
    except Exception as e:
        print(f"❌ Media testing failed: {e}")
        return False

def create_superuser():
    """Create an additional superuser for testing"""
    print("🔄 Creating additional superuser...")
    try:
        if not User.objects.filter(email='superadmin@example.com').exists():
            User.objects.create_user(
                email='superadmin@example.com',
                password='admin123',
                first_name='Super',
                last_name='Admin',
                user_type='admin',
                is_staff=True,
                is_superuser=True
            )
            print("✅ Additional superuser created: superadmin@example.com / admin123")
        else:
            print("ℹ️  Superuser already exists")
        return True
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Starting Django Booking System Setup")
    print("=" * 50)
    
    success = True
    
    # Setup database
    if not setup_database():
        success = False
    
    # Create fixtures
    if success and not create_fixtures():
        success = False
    
    # Load fixtures
    if success and not load_fixtures():
        success = False
        
    # Test loaded data
    if success and not test_data():
        success = False
        
    # Test media functionality
    if success and not test_media():
        success = False
        
    # Create superuser
    if success and not create_superuser():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Setup completed successfully!")
        print("\n📋 Summary:")
        print("- Database migrated and fixtures loaded")
        print("- Sample businesses with services and bookings created")
        print("- QR codes and media files generated")
        print("- User accounts with proper authentication")
        print("\n🔑 Test Accounts:")
        print("- Admin: admin@example.com / password")
        print("- Super Admin: superadmin@example.com / admin123")
        print("- Business Owner: john.doe@example.com / password")
        print("- Customer: mike.wilson@example.com / password")
        print("\n▶️  Start the server: python manage.py runserver")
        print("▶️  Access admin: http://127.0.0.1:8000/admin/")
    else:
        print("❌ Setup failed! Check the errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()