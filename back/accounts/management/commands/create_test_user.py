# accounts/management/commands/create_test_user.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import SubscriptionPlan, Subscription
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a test user for login testing'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, default='admin@email.com')
        parser.add_argument('--password', type=str, default='admin12345')
        parser.add_argument('--first-name', type=str, default='Admin')
        parser.add_argument('--last-name', type=str, default='User')
        parser.add_argument('--user-type', type=str, default='business_owner', 
                          choices=['customer', 'business_owner', 'admin'])
        parser.add_argument('--is-staff', action='store_true', help='Make user staff')
        parser.add_argument('--is-superuser', action='store_true', help='Make user superuser')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']
        user_type = options['user_type']
        is_staff = options['is_staff']
        is_superuser = options['is_superuser']

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email {email} already exists!')
            )
            user = User.objects.get(email=email)
            self.stdout.write(f'User details: {user.email}, active: {user.is_active}')
            self.stdout.write(f'User type: {user.user_type}, staff: {user.is_staff}, superuser: {user.is_superuser}')
            return

        # Create user
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                email_verified=True,
                is_staff=is_staff,
                is_superuser=is_superuser
            )

            # Create free subscription plan if it doesn't exist
            free_plan, created = SubscriptionPlan.objects.get_or_create(
                name='free',
                defaults={
                    'price': 0.00,
                    'max_businesses': 1,
                    'max_services': 5,
                    'max_bookings_per_month': 50,
                    'analytics_enabled': False,
                    'priority_support': False,
                    'custom_branding': False,
                    'api_access': False
                }
            )

            # Create subscription for user
            Subscription.objects.create(
                user=user,
                plan=free_plan,
                status='active',
                current_period_start=timezone.now(),
                current_period_end=timezone.now() + timedelta(days=30)
            )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created admin user: {email}')
            )
            self.stdout.write(f'📧 Email: {email}')
            self.stdout.write(f'🔑 Password: {password}')
            self.stdout.write(f'👤 Name: {first_name} {last_name}')
            self.stdout.write(f'🏢 User Type: {user_type}')
            self.stdout.write(f'🔧 Staff: {is_staff}')
            self.stdout.write(f'⚡ Superuser: {is_superuser}')
            self.stdout.write(f'✨ You can now test login with these credentials!')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating user: {str(e)}')
            )