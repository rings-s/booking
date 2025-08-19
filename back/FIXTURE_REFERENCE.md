# Fixture Data Reference Guide

Quick reference for all UUIDs and relationships in the fixture data.

## User Accounts

| UUID | Email | Type | Plan | Status |
|------|-------|------|------|--------|
| `550e8400-e29b-41d4-a716-446655440010` | admin@example.com | admin | - | Active |
| `550e8400-e29b-41d4-a716-446655440011` | john.doe@example.com | business_owner | Basic | Active |
| `550e8400-e29b-41d4-a716-446655440012` | jane.smith@example.com | business_owner | Premium | Active |
| `550e8400-e29b-41d4-a716-446655440013` | mike.wilson@example.com | customer | Free | Trial |
| `550e8400-e29b-41d4-a716-446655440014` | sarah.johnson@example.com | customer | - | Active |
| `550e8400-e29b-41d4-a716-446655440015` | david.brown@example.com | customer | - | Active |
| `550e8400-e29b-41d4-a716-446655440016` | emma.taylor@example.com | customer | - | Active |

## Subscription Plans

| UUID | Name | Price | Max Businesses | Max Services | Max Bookings/Month |
|------|------|-------|---------------|--------------|-------------------|
| `550e8400-e29b-41d4-a716-446655440001` | free | $0.00 | 1 | 5 | 50 |
| `550e8400-e29b-41d4-a716-446655440002` | basic | $29.99 | 1 | 15 | 200 |
| `550e8400-e29b-41d4-a716-446655440003` | premium | $79.99 | 3 | 50 | 1000 |
| `550e8400-e29b-41d4-a716-446655440004` | enterprise | $199.99 | 10 | 200 | 5000 |

## Businesses

| UUID | Name | Owner | Slug | Category | Location |
|------|------|-------|------|----------|----------|
| `550e8400-e29b-41d4-a716-446655440030` | Elite Hair Studio | john.doe | elite-hair-studio | Beauty & Personal Care | New York, NY |
| `550e8400-e29b-41d4-a716-446655440031` | Wellness Spa & Massage | jane.smith | wellness-spa-massage | Health & Wellness | Los Angeles, CA |
| `550e8400-e29b-41d4-a716-446655440032` | Downtown Dental Care | john.doe | downtown-dental-care | Healthcare | Chicago, IL |

## Services

| UUID | Business | Name | Duration | Price | Description |
|------|----------|------|----------|-------|-------------|
| `550e8400-e29b-41d4-a716-446655440060` | Elite Hair Studio | Haircut & Style | 60min | $65.00 | Professional haircut with styling |
| `550e8400-e29b-41d4-a716-446655440061` | Elite Hair Studio | Hair Color | 120min | $150.00 | Full hair coloring service |
| `550e8400-e29b-41d4-a716-446655440062` | Elite Hair Studio | Highlights | 90min | $120.00 | Professional highlighting service |
| `550e8400-e29b-41d4-a716-446655440063` | Wellness Spa | Swedish Massage | 60min | $90.00 | Relaxing Swedish massage |
| `550e8400-e29b-41d4-a716-446655440064` | Wellness Spa | Deep Tissue Massage | 90min | $130.00 | Therapeutic deep tissue massage |
| `550e8400-e29b-41d4-a716-446655440065` | Wellness Spa | Facial Treatment | 75min | $110.00 | Luxurious facial treatment |
| `550e8400-e29b-41d4-a716-446655440066` | Downtown Dental | Dental Cleaning | 45min | $125.00 | Professional dental cleaning |
| `550e8400-e29b-41d4-a716-446655440067` | Downtown Dental | Dental Consultation | 30min | $75.00 | Initial consultation with dentist |

## Customer Profiles

| UUID | User | Phone | Total Bookings | Total Spent | Preferred Businesses |
|------|------|-------|---------------|-------------|-------------------|
| `550e8400-e29b-41d4-a716-446655440070` | mike.wilson | +1-555-1234 | 5 | $425.00 | Elite Hair Studio, Wellness Spa |
| `550e8400-e29b-41d4-a716-446655440071` | sarah.johnson | +1-555-5678 | 3 | $320.00 | Wellness Spa |
| `550e8400-e29b-41d4-a716-446655440072` | david.brown | +1-555-9012 | 2 | $200.00 | Downtown Dental |
| `550e8400-e29b-41d4-a716-446655440073` | emma.taylor | +1-555-3456 | 1 | $65.00 | None |

## Bookings

| UUID | Business | Customer | Service | Date | Time | Status | Price | Paid |
|------|----------|----------|---------|------|------|--------|-------|------|
| `550e8400-e29b-41d4-a716-446655440080` | Elite Hair Studio | mike.wilson | Haircut & Style | 2024-01-15 | 10:00 | completed | $65.00 | ✅ |
| `550e8400-e29b-41d4-a716-446655440081` | Elite Hair Studio | mike.wilson | Hair Color | 2024-02-01 | 14:00 | confirmed | $150.00 | ❌ |
| `550e8400-e29b-41d4-a716-446655440082` | Wellness Spa | sarah.johnson | Swedish Massage | 2024-01-20 | 15:30 | completed | $90.00 | ✅ |
| `550e8400-e29b-41d4-a716-446655440083` | Wellness Spa | sarah.johnson | Deep Tissue Massage | 2024-02-05 | 11:00 | confirmed | $130.00 | ✅ |
| `550e8400-e29b-41d4-a716-446655440084` | Downtown Dental | david.brown | Dental Cleaning | 2024-01-18 | 09:00 | completed | $125.00 | ✅ |
| `550e8400-e29b-41d4-a716-446655440085` | Elite Hair Studio | emma.taylor | Haircut & Style | 2024-02-10 | 16:00 | pending | $65.00 | ❌ |

## Reviews

| UUID | Business | Customer | Booking | Rating | Title | Featured |
|------|----------|----------|---------|--------|-------|----------|
| `550e8400-e29b-41d4-a716-446655440090` | Elite Hair Studio | mike.wilson | Haircut (completed) | 5⭐ | Amazing Experience! | ✅ |
| `550e8400-e29b-41d4-a716-446655440091` | Wellness Spa | sarah.johnson | Swedish Massage | 4⭐ | Very Relaxing | ❌ |
| `550e8400-e29b-41d4-a716-446655440092` | Downtown Dental | david.brown | Dental Cleaning | 5⭐ | Professional and Thorough | ✅ |

## Notifications

| UUID | User | Type | Title | Read | Related Booking |
|------|------|------|-------|------|----------------|
| `550e8400-e29b-41d4-a716-446655440100` | mike.wilson | booking_confirmed | Booking Confirmed | ❌ | Hair Color (confirmed) |
| `550e8400-e29b-41d4-a716-446655440101` | sarah.johnson | booking_reminder | Appointment Reminder | ✅ | Deep Tissue Massage |
| `550e8400-e29b-41d4-a716-446655440102` | john.doe | new_customer | New Customer Registration | ❌ | Emma's first booking |
| `550e8400-e29b-41d4-a716-446655440103` | mike.wilson | review_request | How was your service? | ❌ | Completed haircut |

## Business Hours

### Elite Hair Studio
- **Monday-Thursday**: 9:00 AM - 7:00 PM
- **Friday-Saturday**: 9:00 AM - 8:00 PM
- **Sunday**: 10:00 AM - 5:00 PM

### Wellness Spa & Massage
- **Monday-Saturday**: 8:00 AM - 9:00 PM
- **Sunday**: 9:00 AM - 8:00 PM

### Downtown Dental Care
- Standard business hours (configured via fixtures)

## Media Files Generated

When running the test script, these files will be created:

### QR Codes
- `media/qr_codes/qr_elite-hair-studio.png`
- `media/qr_codes/qr_wellness-spa-massage.png`
- `media/qr_codes/qr_downtown-dental-care.png`

### Logos
- `media/business_logos/logo_elite-hair-studio.png`
- `media/business_logos/logo_wellness-spa-massage.png`
- `media/business_logos/logo_downtown-dental-care.png`

### Cover Images
- `media/business_covers/cover_elite-hair-studio.png`
- `media/business_covers/cover_wellness-spa-massage.png`
- `media/business_covers/cover_downtown-dental-care.png`

## Relationship Mapping

```
Users (7 total)
├── admin@example.com (Admin)
├── john.doe@example.com (Business Owner)
│   ├── Subscription: Basic Plan
│   ├── Businesses: Elite Hair Studio, Downtown Dental Care
│   └── Receives: New Customer Notifications
├── jane.smith@example.com (Business Owner)
│   ├── Subscription: Premium Plan
│   └── Business: Wellness Spa & Massage
└── Customers (4 total)
    ├── mike.wilson@example.com
    │   ├── Subscription: Free Trial
    │   ├── Bookings: 2 (1 completed, 1 confirmed)
    │   ├── Reviews: 1 (5-star for Elite Hair)
    │   └── Notifications: 2
    ├── sarah.johnson@example.com
    │   ├── Bookings: 2 (1 completed, 1 confirmed)
    │   ├── Reviews: 1 (4-star for Wellness Spa)
    │   └── Notifications: 1
    ├── david.brown@example.com
    │   ├── Bookings: 1 (completed)
    │   └── Reviews: 1 (5-star for Downtown Dental)
    └── emma.taylor@example.com
        └── Bookings: 1 (pending, first customer)
```

This fixture data provides a comprehensive testing environment with realistic business scenarios, customer interactions, and system relationships.