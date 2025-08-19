# Django Booking System - Complete Setup Guide

This guide provides step-by-step instructions to set up the Django booking system with comprehensive dummy data, proper admin configuration, and working media files.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Navigate to the backend directory
cd /path/to/booking/back

# Run the complete setup script
./run_tests.sh
```

### Option 2: Manual Step-by-Step

```bash
# 1. Run database migrations
python manage.py migrate

# 2. Create fixtures with proper password hashes
python manage.py create_fixtures

# 3. Load accounts data
python manage.py loaddata accounts/fixtures/accounts_data.json

# 4. Load business/booking data
python manage.py loaddata base/fixtures/base_data.json

# 5. Generate QR codes and media files
python manage.py test_media_qr

# 6. Check admin registration
python manage.py check_admin

# 7. Start the development server
python manage.py runserver
```

## 📊 What Gets Created

### User Accounts (All passwords: 'password')

| Email | Type | Role | Subscription |
|-------|------|------|--------------|
| admin@example.com | Admin | System Administrator | - |
| john.doe@example.com | Business Owner | Owns 2 businesses | Basic Plan |
| jane.smith@example.com | Business Owner | Owns 1 business | Premium Plan |
| mike.wilson@example.com | Customer | Regular customer | Free Trial |
| sarah.johnson@example.com | Customer | Premium customer | - |
| david.brown@example.com | Customer | Dental patient | - |
| emma.taylor@example.com | Customer | New customer | - |

### Subscription Plans

- **Free Plan**: $0/month, 1 business, 5 services, 50 bookings
- **Basic Plan**: $29.99/month, 1 business, 15 services, 200 bookings
- **Premium Plan**: $79.99/month, 3 businesses, 50 services, 1000 bookings
- **Enterprise Plan**: $199.99/month, 10 businesses, 200 services, 5000 bookings

### Businesses with Complete Data

1. **Elite Hair Studio** (New York)
   - Owner: john.doe@example.com
   - Services: Haircut ($65), Hair Color ($150), Highlights ($120)
   - Hours: Mon-Thu 9am-7pm, Fri-Sat 9am-8pm, Sun 10am-5pm

2. **Wellness Spa & Massage** (Los Angeles)
   - Owner: jane.smith@example.com
   - Services: Swedish Massage ($90), Deep Tissue ($130), Facial ($110)
   - Hours: Mon-Sat 8am-9pm, Sun 9am-8pm

3. **Downtown Dental Care** (Chicago)
   - Owner: john.doe@example.com
   - Services: Dental Cleaning ($125), Consultation ($75)

### Sample Bookings & Reviews

- 6 bookings with various statuses (completed, confirmed, pending)
- 3 detailed reviews with business responses
- 4 notifications covering different scenarios
- Customer profiles with booking history and preferences

### Media Files Generated

- QR codes for each business (linking to booking pages)
- Sample business logos (colored backgrounds with initials)
- Sample cover images (branded backgrounds)
- Organized in `media/` directory structure

## 🔧 Admin Interface Access

### Login to Admin Panel

1. **Start the server**: `python manage.py runserver`
2. **Visit**: http://127.0.0.1:8000/admin/
3. **Login with**:
   - Email: `admin@example.com`
   - Password: `password`

### Admin Panel Features

#### Accounts Section
- **Users**: View all user accounts, manage permissions
- **Subscription Plans**: Configure pricing and features
- **Subscriptions**: Monitor active subscriptions

#### Base Section
- **Businesses**: Complete business management with inline services/hours
- **Services**: Service catalog with pricing
- **Customers**: Customer profiles with booking history
- **Bookings**: Booking management with status tracking
- **Reviews**: Review moderation and business responses
- **Notifications**: Notification system management

## 🧪 Testing & Verification

### Verify Data Loading

```bash
# Check admin registration
python manage.py check_admin

# Verify user authentication
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> user = User.objects.get(email='admin@example.com')
>>> user.check_password('password')  # Should return True
```

### Test Authentication

1. **Admin Login**: Use admin@example.com / password
2. **Business Owner Login**: Use john.doe@example.com / password
3. **Customer Login**: Use mike.wilson@example.com / password

### Verify Media Files

```bash
# Check media directory structure
ls -la media/
ls -la media/qr_codes/
ls -la media/business_logos/
ls -la media/business_covers/
```

## 🔍 Troubleshooting

### Issue: "No data visible in admin"

**Solution**:
```bash
# Reload fixtures
python manage.py flush --noinput
python manage.py migrate
./run_tests.sh
```

### Issue: "Password authentication failed"

**Solution**: Fixtures include proper PBKDF2 password hashes. All test accounts use password: `password`

### Issue: "Media files not generating"

**Solution**:
```bash
# Ensure media directory exists
mkdir -p media/qr_codes media/business_logos media/business_covers

# Regenerate media files
python manage.py test_media_qr
```

### Issue: "Admin models not appearing"

**Solution**: Check that both apps are in `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'accounts',
    'base',
    # ...
]
```

## 📱 API Testing

### Sample API Endpoints (when authentication is configured)

```bash
# Get businesses
curl http://localhost:8000/api/businesses/

# Get services for a business
curl http://localhost:8000/api/businesses/elite-hair-studio/services/

# Get user profile (requires authentication)
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/accounts/profile/
```

## 🔄 Data Relationships

The fixture data maintains proper foreign key relationships:

- Users → Subscriptions (one-to-one)
- Users → Businesses (one-to-many for business owners)
- Users → Customer profiles (one-to-one for customers)
- Businesses → Services (one-to-many)
- Businesses → Business Hours (one-to-many)
- Businesses → Bookings (one-to-many)
- Customers → Bookings (one-to-many)
- Services → Bookings (one-to-many)
- Bookings → Reviews (one-to-one)
- Bookings → Notifications (one-to-many)

## 📋 Next Steps

1. **Customize Data**: Modify fixtures to match your specific business needs
2. **Add Authentication**: Configure JWT tokens for API access
3. **Frontend Integration**: Connect SvelteKit frontend with backend APIs
4. **Email Configuration**: Set up email for notifications
5. **Payment Integration**: Configure Stripe for subscriptions
6. **Production Setup**: Configure PostgreSQL, Redis, and media storage

## 🛠️ Development Commands

```bash
# Create new fixtures after model changes
python manage.py dumpdata accounts --indent 2 > accounts/fixtures/new_accounts.json
python manage.py dumpdata base --indent 2 > base/fixtures/new_base.json

# Reset database completely
python manage.py flush --noinput
python manage.py migrate
./run_tests.sh

# Create additional test data
python manage.py shell
# ... use Django ORM to create additional objects
```

This setup provides a complete, realistic development environment for the Django booking system with proper admin access, authentication, and sample data relationships.