# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, SubscriptionPlan, Subscription

# Register the User model with a custom admin class
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin class for the User model.
    """
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'user_type', 'email_verified')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Verification', {'fields': ('email_verified',)}),
    )

    # Use the custom `UserCreationForm` and `UserChangeForm` if you have them.
    # Otherwise, this is a good default setup.
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login', 'date_joined')


# Register the SubscriptionPlan model
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin class for SubscriptionPlan model.
    """
    list_display = ('name', 'price', 'stripe_price_id', 'max_services', 'analytics_enabled')
    list_filter = ('name', 'analytics_enabled', 'priority_support', 'custom_branding')
    search_fields = ('name', 'stripe_price_id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'stripe_price_id')
        }),
        ('Features', {
            'fields': (
                'max_services',
                'max_bookings_per_month',
                'max_staff_accounts',
                'analytics_enabled',
                'priority_support',
                'custom_branding',
                'api_access'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


# Register the Subscription model
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin class for Subscription model.
    """
    list_display = ('user', 'plan', 'status', 'is_active', 'current_period_end')
    list_filter = ('status', 'plan')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'stripe_subscription_id')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'current_period_end'
    list_select_related = ('user', 'plan')

    fieldsets = (
        (None, {
            'fields': ('user', 'plan', 'status')
        }),
        ('Stripe Details', {
            'fields': ('stripe_subscription_id', 'stripe_customer_id'),
            'classes': ('collapse',)
        }),
        ('Subscription Dates', {
            'fields': ('trial_end', 'current_period_start', 'current_period_end')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )