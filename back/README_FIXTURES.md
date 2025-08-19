# Django Fixtures for Booking Management System

This directory contains comprehensive fixtures for testing and development of the booking management system.

## Fixtures Overview

### Accounts App (`accounts/fixtures/accounts_data.json`)

**Subscription Plans:**
- Free Plan: $0/month, 1 business, 5 services, 50 bookings/month
- Basic Plan: $29.99/month, 1 business, 15 services, 200 bookings/month
- Premium Plan: $79.99/month, 3 businesses, 50 services, 1000 bookings/month
- Enterprise Plan: $199.99/month, 10 businesses, 200 services, 5000 bookings/month

**User Accounts:**
| Email | Password | Type | Status |
|-------|----------|------|--------|
| admin@example.com | password | Admin | Active |
| john.doe@example.com | password | Business Owner | Active (Basic Plan) |
| jane.smith@example.com | password | Business Owner | Active (Premium Plan) |
| mike.wilson@example.com | password | Customer | Trial (Free Plan) |
| sarah.johnson@example.com | password | Customer | Active |
| david.brown@example.com | password | Customer | Active |
| emma.taylor@example.com | password | Customer | Active |

### Base App (`base/fixtures/base_data.json`)

**Businesses:**
1. **Elite Hair Studio** (Owner: john.doe@example.com)
   - Category: Beauty & Personal Care
   - Location: New York, NY
   - Services: Haircut & Style ($65), Hair Color ($150), Highlights ($120)
   - Hours: Mon-Thu 9am-7pm, Fri-Sat 9am-8pm, Sun 10am-5pm

2. **Wellness Spa & Massage** (Owner: jane.smith@example.com)
   - Category: Health & Wellness
   - Location: Los Angeles, CA
   - Services: Swedish Massage ($90), Deep Tissue Massage ($130), Facial Treatment ($110)
   - Hours: Daily 8am-9pm, Sun 9am-8pm

3. **Downtown Dental Care** (Owner: john.doe@example.com)
   - Category: Healthcare
   - Location: Chicago, IL
   - Services: Dental Cleaning ($125), Dental Consultation ($75)
   - Hours: Standard dental office hours

**Sample Data Includes:**
- 4 Customer profiles with preferences and booking history
- 6+ Bookings with various statuses (pending, confirmed, completed)
- 3 Reviews with business responses
- 4 Notifications for different scenarios
- Complete business hours for all businesses

## Loading Fixtures

### Option 1: Individual Loading
```bash
# Load accounts data first (required dependencies)
python manage.py loaddata accounts/fixtures/accounts_data.json

# Load base app data
python manage.py loaddata base/fixtures/base_data.json

# Test media and QR code generation
python manage.py test_media_qr
```

### Option 2: Automated Script
```bash
# Make sure you're in the Django project root
chmod +x test_fixtures.sh
./test_fixtures.sh
```

### Option 3: Python Script
```bash
python load_fixtures.py
```

## Media Files & QR Codes

The fixtures system includes:

- **QR Code Generation**: Automatic QR codes for each business linking to their booking page
- **Sample Images**: Programmatically generated logos and cover images
- **Media Directories**: Properly organized under `media/business_logos/`, `media/business_covers/`, `media/qr_codes/`

## Testing Features

After loading fixtures, you can test:

1. **Authentication**: Login with any user account (password: "password")
2. **Business Management**: john.doe@example.com owns Elite Hair Studio and Downtown Dental Care
3. **Customer Bookings**: Customer accounts have existing booking history
4. **Reviews & Ratings**: Sample reviews with business responses
5. **Notifications**: Various notification types and statuses
6. **QR Code Access**: Each business has a functional QR code
7. **Media Files**: Logo and cover images are generated automatically

## API Testing

Use these accounts to test different API endpoints:

- **Admin Access**: admin@example.com (full system access)
- **Business Owner**: john.doe@example.com (manage 2 businesses)
- **Premium Business**: jane.smith@example.com (premium features)
- **Customer**: mike.wilson@example.com (customer perspective)

## Development Tips

1. **Password**: All accounts use "password" for development
2. **Email Verification**: Most accounts are pre-verified
3. **Subscriptions**: Various subscription statuses for testing billing features
4. **Data Relationships**: All foreign keys properly linked for realistic testing
5. **Media URLs**: Media files accessible at `/media/` endpoint

## Troubleshooting

If fixtures fail to load:

1. Ensure migrations are up to date: `python manage.py migrate`
2. Check for existing data conflicts
3. Use `--verbosity=2` flag for detailed loading information
4. Verify media directory permissions

## Fixture Maintenance

To update fixtures:

1. Modify the JSON files directly
2. Or use `python manage.py dumpdata` after making changes via Django admin
3. Always maintain referential integrity between models
4. Update this README when adding new fixture data