#!/usr/bin/env python
"""
Script to load all fixtures and test media/QR code functionality
Usage: python load_fixtures.py
"""
import os
import sys
import django
from django.core.management import call_command
from django.conf import settings

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')
django.setup()

def main():
    """Load fixtures and test media functionality"""
    print("🚀 Starting fixture loading and media testing...")
    print("=" * 60)
    
    try:
        # Check if we need to migrate first
        print("📊 Checking database migrations...")
        call_command('migrate', verbosity=1)
        
        # Load accounts fixtures first (dependencies)
        print("\n👥 Loading accounts fixtures...")
        call_command('loaddata', 'accounts/fixtures/accounts_data.json', verbosity=2)
        
        # Load base fixtures
        print("\n🏢 Loading base app fixtures...")
        call_command('loaddata', 'base/fixtures/base_data.json', verbosity=2)
        
        # Test media and QR code functionality
        print("\n📱 Testing media and QR code generation...")
        call_command('test_media_qr', verbosity=2)
        
        print("\n" + "=" * 60)
        print("✅ All fixtures loaded and media functionality tested successfully!")
        print("\nSample accounts created:")
        print("- Admin: admin@example.com / password")
        print("- Business Owner: john.doe@example.com / password")
        print("- Business Owner: jane.smith@example.com / password")
        print("- Customers: mike.wilson@example.com, sarah.johnson@example.com, etc.")
        print("\nSample businesses:")
        print("- Elite Hair Studio (Hair Salon)")
        print("- Wellness Spa & Massage (Spa)")
        print("- Downtown Dental Care (Dental)")
        print("\n🔗 QR codes generated for all businesses")
        print("🖼️  Sample logos and cover images created")
        print("\nYou can now start the Django development server:")
        print("python manage.py runserver")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure you're in the Django project directory and all dependencies are installed.")
        sys.exit(1)

if __name__ == '__main__':
    main()