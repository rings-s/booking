# base/utils.py
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
import uuid

def generate_qr_code_with_logo(data, logo_path=None):
    """Generate QR code with optional logo"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    if logo_path:
        logo = Image.open(logo_path)
        
        # Calculate logo size (10% of QR code)
        basewidth = int(img.size[0] * 0.2)
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
        
        # Position logo in center
        pos = ((img.size[0] - logo.size[0]) // 2,
               (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos)
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    file_name = f'qr_{uuid.uuid4()}.png'
    
    return File(buffer, name=file_name)


def send_booking_reminder(booking):
    """Send booking reminder notification"""
    from .models import Notification
    
    Notification.objects.create(
        user=booking.customer.user,
        type='booking_reminder',
        title='Booking Reminder',
        message=f'Reminder: You have a booking for {booking.service.name} tomorrow at {booking.start_time}',
        booking=booking,
        business=booking.business
    )


def calculate_available_slots(business, service, date):
    """Calculate available booking slots for a service on a specific date"""
    from .models import Booking, BusinessHours
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    weekday = date.weekday()
    
    try:
        hours = BusinessHours.objects.get(business=business, weekday=weekday)
        if hours.is_closed:
            return []
    except BusinessHours.DoesNotExist:
        return []
    
    # Don't allow booking in the past
    now = timezone.now()
    current_date = now.date()
    current_time = now.time()
    
    if date < current_date:
        return []
    
    # Get existing bookings
    existing_bookings = Booking.objects.filter(
        business=business,
        service=service,
        booking_date=date,
        status__in=['confirmed', 'pending']
    ).values_list('start_time', 'end_time')
    
    # Generate available slots
    available_slots = []
    slot_start_time = timezone.make_aware(datetime.combine(date, hours.opening_time))
    closing_time = timezone.make_aware(datetime.combine(date, hours.closing_time))
    service_duration = timedelta(minutes=service.duration_minutes)
    buffer_duration = timedelta(minutes=service.buffer_time_minutes)
    slot_increment = service_duration + buffer_duration
    
    # If booking for today, start from current time + 1 hour minimum
    if date == current_date:
        min_booking_time = now + timedelta(hours=1)
        if slot_start_time < min_booking_time:
            # Round up to next slot
            minutes_diff = (min_booking_time - slot_start_time).total_seconds() / 60
            slots_to_skip = int(minutes_diff / slot_increment.total_seconds() * 60) + 1
            slot_start_time += slot_increment * slots_to_skip
    
    current_slot_time = slot_start_time
    
    while current_slot_time + service_duration <= closing_time:
        slot_start = current_slot_time.time()
        slot_end = (current_slot_time + service_duration).time()
        
        # Check if slot conflicts with existing bookings
        is_available = True
        for booking_start, booking_end in existing_bookings:
            if not (slot_end <= booking_start or slot_start >= booking_end):
                is_available = False
                break
        
        if is_available:
            available_slots.append({
                'start_time': slot_start.strftime('%H:%M'),
                'end_time': slot_end.strftime('%H:%M'),
                'available_spots': service.max_bookings_per_slot - len([
                    b for b in existing_bookings 
                    if not (slot_end <= b[0] or slot_start >= b[1])
                ])
            })
        
        current_slot_time += slot_increment
    
    return available_slots


def get_available_dates(business, service, start_date=None, days_ahead=90):
    """Get available dates for a service within the next specified days"""
    from .models import BusinessHours
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    if start_date is None:
        start_date = timezone.now().date()
    
    available_dates = []
    current_date = start_date
    end_date = start_date + timedelta(days=days_ahead)
    
    # Get business hours for all weekdays
    business_hours = {
        bh.weekday: bh for bh in BusinessHours.objects.filter(business=business)
    }
    
    while current_date <= end_date:
        weekday = current_date.weekday()
        
        # Check if business is open on this day
        if weekday in business_hours and not business_hours[weekday].is_closed:
            # Check if there are any available slots
            slots = calculate_available_slots(business, service, current_date)
            if slots:
                available_dates.append({
                    'date': current_date.isoformat(),
                    'weekday': current_date.strftime('%A'),
                    'slots_count': len(slots)
                })
        
        current_date += timedelta(days=1)
    
    return available_dates