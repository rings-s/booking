#!/bin/bash

# Complete setup and test script for Django booking system
echo "🚀 Django Booking System - Complete Setup & Test"
echo "================================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the Django project root directory"
    exit 1
fi

# Function to run Django commands and check results
run_command() {
    echo "🔄 $1"
    if eval "$2"; then
        echo "✅ $1 completed successfully"
        return 0
    else
        echo "❌ $1 failed"
        return 1
    fi
}

# Setup database
run_command "Setting up database migrations" "python manage.py migrate --verbosity=1"
if [ $? -ne 0 ]; then exit 1; fi

# Create fixtures with proper password hashes
run_command "Creating fixtures with proper password hashes" "python manage.py create_fixtures"
if [ $? -ne 0 ]; then exit 1; fi

# Load accounts fixtures
run_command "Loading accounts fixtures" "python manage.py loaddata accounts/fixtures/accounts_data.json --verbosity=1"
if [ $? -ne 0 ]; then exit 1; fi

# Load base fixtures
run_command "Loading base app fixtures" "python manage.py loaddata base/fixtures/base_data.json --verbosity=1"
if [ $? -ne 0 ]; then exit 1; fi

# Test media and QR code generation
run_command "Testing media and QR code generation" "python manage.py test_media_qr"
if [ $? -ne 0 ]; then exit 1; fi

# Run the comprehensive test
run_command "Running comprehensive data tests" "python setup_and_test.py"
if [ $? -ne 0 ]; then exit 1; fi

echo ""
echo "================================================="
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 What was created:"
echo "✓ Database with all required tables"
echo "✓ 4 Subscription plans (Free, Basic, Premium, Enterprise)"
echo "✓ 7 User accounts with proper password hashing"
echo "✓ 3 Businesses with complete profiles"
echo "✓ 8 Services across different business types"
echo "✓ 4 Customer profiles with booking history"
echo "✓ 6 Bookings with various statuses"
echo "✓ 3 Reviews with business responses"
echo "✓ 4 Notifications for different scenarios"
echo "✓ QR codes generated for all businesses"
echo "✓ Sample logos and cover images created"
echo ""
echo "🔑 Test Accounts (password: 'password'):"
echo "   Admin: admin@example.com"
echo "   Business Owner: john.doe@example.com"
echo "   Business Owner: jane.smith@example.com"
echo "   Customer: mike.wilson@example.com"
echo ""
echo "🌐 Next steps:"
echo "   1. Start the server: python manage.py runserver"
echo "   2. Visit admin panel: http://127.0.0.1:8000/admin/"
echo "   3. Login with admin@example.com / password"
echo ""
echo "📁 Media files created in:"
echo "   - media/business_logos/"
echo "   - media/business_covers/"
echo "   - media/qr_codes/"