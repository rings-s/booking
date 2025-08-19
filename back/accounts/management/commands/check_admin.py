"""
Management command to check admin registration and permissions
"""
from django.core.management.base import BaseCommand
from django.contrib import admin
from django.apps import apps


class Command(BaseCommand):
    help = 'Check admin registration and permissions'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking admin registration...'))
        
        # Check registered models
        registered_models = admin.site._registry
        
        self.stdout.write(f"\n📋 Registered Admin Models ({len(registered_models)}):")
        
        for model, model_admin in registered_models.items():
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            admin_class = model_admin.__class__.__name__
            
            self.stdout.write(f"  ✓ {app_label}.{model_name} -> {admin_class}")
        
        # Check accounts models specifically
        accounts_models = [
            'User',
            'SubscriptionPlan', 
            'Subscription'
        ]
        
        base_models = [
            'Business',
            'BusinessHours',
            'Service',
            'Customer',
            'Booking',
            'Review',
            'Notification'
        ]
        
        self.stdout.write(f"\n👥 Accounts App Models:")
        accounts_app = apps.get_app_config('accounts')
        for model in accounts_app.get_models():
            model_name = model.__name__
            is_registered = model in registered_models
            status = "✅ Registered" if is_registered else "❌ Not Registered"
            self.stdout.write(f"  {model_name}: {status}")
        
        self.stdout.write(f"\n🏢 Base App Models:")
        base_app = apps.get_app_config('base')
        for model in base_app.get_models():
            model_name = model.__name__
            is_registered = model in registered_models
            status = "✅ Registered" if is_registered else "❌ Not Registered"
            self.stdout.write(f"  {model_name}: {status}")
        
        self.stdout.write(f"\n✅ Admin check completed!")
        self.stdout.write(f"🔗 Admin URL: /admin/")