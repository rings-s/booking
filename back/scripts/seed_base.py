from datetime import timedelta, time, date
from django.utils import timezone
from django.contrib.auth import get_user_model
from base.models import Business, BusinessHours, Service, Customer, Booking, Review, Notification

User = get_user_model()

def run():
    # Pick existing users seeded earlier
    owner = User.objects.filter(email="owner@example.com").first()
    customer_user = User.objects.filter(email="customer@example.com").first()
    if not owner or not customer_user:
        print("Required users not found. Seed accounts first.")
        return

    # Ensure Customer profile exists
    customer, _ = Customer.objects.update_or_create(
        user=customer_user,
        defaults={
            "phone": "+1 555-0100",
            "receive_notifications": True,
            "receive_marketing_emails": False,
        },
    )

    # Business
    biz_defaults = {
        "owner": owner,
        "description": "Premium wellness & spa services with expert staff.",
        "email": "hello@wellness.example",
        "phone": "+1 555-0200",
        "website": "https://wellness.example",
        "address": "123 Main St",
        "city": "San Francisco",
        "state": "CA",
        "country": "USA",
        "postal_code": "94105",
        "category": "Wellness & Spa",
        "is_active": True,
        "accepts_online_bookings": True,
        "auto_confirm_bookings": True,
    }
    business, _ = Business.objects.update_or_create(
        slug="wellness-spa",
        defaults={"name": "Wellness Spa", **biz_defaults},
    )

    # Business hours (Mon-Sun 9am-6pm)
    for weekday in range(7):
        BusinessHours.objects.update_or_create(
            business=business,
            weekday=weekday,
            defaults={
                "opening_time": time(9, 0),
                "closing_time": time(18, 0),
                "is_closed": False if weekday < 6 else False,
            },
        )

    # Services
    massage, _ = Service.objects.update_or_create(
        business=business,
        name="Full Body Massage",
        defaults={
            "description": "60-minute relaxing massage",
            "duration_minutes": 60,
            "price": 80,
            "is_active": True,
            "max_bookings_per_slot": 1,
            "buffer_time_minutes": 10,
        },
    )
    facial, _ = Service.objects.update_or_create(
        business=business,
        name="Facial Treatment",
        defaults={
            "description": "45-minute cleansing facial",
            "duration_minutes": 45,
            "price": 65,
            "is_active": True,
            "max_bookings_per_slot": 1,
            "buffer_time_minutes": 5,
        },
    )

    # Customer preferences
    customer.preferred_businesses.add(business)

    # Booking for tomorrow 10:00-11:00
    tomorrow = date.today() + timedelta(days=1)
    start = time(10, 0)
    end = time(11, 0)
    booking, _ = Booking.objects.update_or_create(
        business=business,
        customer=customer,
        service=massage,
        booking_date=tomorrow,
        start_time=start,
        defaults={
            "end_time": end,
            "status": "confirmed",
            "notes": "Please prepare a quiet room.",
            "total_price": massage.price,
            "is_paid": True,
            "payment_method": "card",
            "payment_id": "TESTPAY123",
        },
    )

    # Review linked to booking (if not already)
    Review.objects.update_or_create(
        business=business,
        customer=customer,
        booking=booking,
        defaults={
            "rating": 5,
            "title": "Amazing experience",
            "comment": "Felt completely relaxed. Highly recommended!",
            "is_verified": True,
            "is_featured": True,
            "business_response": "Thank you for visiting us!",
            "response_date": timezone.now(),
        },
    )

    # Notification for the owner
    Notification.objects.update_or_create(
        user=owner,
        title="New booking confirmed",
        defaults={
            "type": "booking_confirmed",
            "message": f"Booking confirmed for {customer_user.email} at {business.name}",
            "business": business,
            "booking": booking,
            "is_read": False,
            "send_email": True,
            "send_push": False,
            "email_sent": False,
            "push_sent": False,
        },
    )

    print("Base seeding done.")

if __name__ == "__main__":
    run()
