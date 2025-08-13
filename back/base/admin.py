# base/admin.py
from django.contrib import admin
from .models import Business, BusinessHours, Service, Customer, Booking, Review, Notification

# Inlines for a better admin experience
class BusinessHoursInline(admin.TabularInline):
    """
    Inline for BusinessHours to be displayed within the Business admin page.
    """
    model = BusinessHours
    extra = 1  # Number of extra forms to display

class ServiceInline(admin.TabularInline):
    """
    Inline for Services to be displayed within the Business admin page.
    """
    model = Service
    extra = 1

class BookingInline(admin.TabularInline):
    """
    Inline for Bookings to be displayed within the Business and Customer admin pages.
    """
    model = Booking
    extra = 0
    readonly_fields = ('booking_date', 'start_time', 'end_time', 'service', 'total_price', 'status')
    can_delete = False
    show_change_link = True

class ReviewInline(admin.TabularInline):
    """
    Inline for Reviews to be displayed within the Business and Customer admin pages.
    """
    model = Review
    extra = 0
    readonly_fields = ('rating', 'title', 'comment', 'created_at')
    can_delete = False
    show_change_link = True

# Custom Admin Models
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'phone', 'address')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BusinessHoursInline, ServiceInline]
    readonly_fields = ('qr_code', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('owner', 'name', 'slug', 'description')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'website'),
            'classes': ('collapse',)
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code'),
            'classes': ('collapse',)
        }),
        ('Business Details', {
            'fields': ('category', 'logo', 'cover_image', 'qr_code'),
            'classes': ('wide',)
        }),
        ('Settings', {
            'fields': ('is_active', 'accepts_online_bookings', 'auto_confirm_bookings'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'duration_minutes', 'price', 'is_active')
    list_filter = ('business', 'is_active')
    search_fields = ('name', 'business__name')
    list_select_related = ('business',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_first_name', 'phone', 'total_bookings', 'total_spent', 'receive_notifications')
    list_filter = ('receive_notifications', 'receive_marketing_emails')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'total_bookings', 'total_spent')
    inlines = [BookingInline, ReviewInline]

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    def user_first_name(self, obj):
        return obj.user.first_name
    user_first_name.short_description = 'First Name'

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'business', 'service', 'booking_date', 'start_time', 'status', 'is_paid')
    list_filter = ('status', 'is_paid', 'business', 'service')
    search_fields = ('customer__user__email', 'business__name', 'service__name')
    readonly_fields = ('created_at', 'updated_at', 'total_price')
    list_select_related = ('customer__user', 'business', 'service')
    date_hierarchy = 'booking_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('business', 'customer', 'rating', 'title', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'is_featured', 'business')
    search_fields = ('title', 'comment', 'business__name', 'customer__user__email')
    readonly_fields = ('created_at', 'updated_at', 'business_response', 'response_date')
    list_select_related = ('business', 'customer__user')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'title', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'send_email', 'send_push')
    search_fields = ('user__email', 'title', 'message')
    readonly_fields = ('created_at', 'read_at', 'email_sent', 'push_sent')
    list_select_related = ('user',)

# Register BusinessHours and Service inline with Business so they are not top-level admin pages
# admin.site.register(BusinessHours)
# If you prefer BusinessHours and Service as top-level admin pages, uncomment the lines above.