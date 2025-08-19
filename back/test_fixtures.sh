#!/bin/bash
# Test script for loading fixtures and testing media functionality

echo "🚀 Testing fixture loading and media functionality..."
echo "============================================================"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the Django project root."
    exit 1
fi

# Run migrations first
echo "📊 Running database migrations..."
python manage.py migrate

# Load accounts fixtures
echo ""
echo "👥 Loading accounts fixtures..."
python manage.py loaddata accounts/fixtures/accounts_data.json

# Load base fixtures  
echo ""
echo "🏢 Loading base app fixtures..."
python manage.py loaddata base/fixtures/base_data.json

# Test media and QR code functionality
echo ""
echo "📱 Testing media and QR code generation..."
python manage.py test_media_qr

echo ""
echo "============================================================"
echo "✅ Fixture loading and testing completed!"
echo ""
echo "Sample accounts created:"
echo "- Admin: admin@example.com (password: password)"
echo "- Business Owner: john.doe@example.com (password: password)"
echo "- Business Owner: jane.smith@example.com (password: password)"
echo "- Customers: mike.wilson@example.com, sarah.johnson@example.com, etc."
echo ""
echo "Sample businesses with services and bookings:"
echo "- Elite Hair Studio (Hair Salon)"
echo "- Wellness Spa & Massage (Spa)"
echo "- Downtown Dental Care (Dental)"
echo ""
echo "🔗 QR codes generated for all businesses"
echo "🖼️  Sample logos and cover images created"
echo ""
echo "You can now start the Django development server:"
echo "python manage.py runserver"