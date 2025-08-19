# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Subscription, SubscriptionPlan
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from django.conf import settings

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 
                 'user_type', 'email_verified', 'date_joined', 'is_staff', 'is_superuser']
        read_only_fields = ['id', 'email_verified', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 
                 'password_confirm', 'user_type']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)
    
    def validate(self, attrs):
        import logging
        logger = logging.getLogger(__name__)
        
        email = attrs.get('email')
        password = attrs.get('password')
        
        logger.info(f"Login validation attempt for email: {email}")
        
        if not email or not password:
            raise serializers.ValidationError('Email and password are required')
        
        # Check if user exists first
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user_exists = User.objects.filter(email=email).exists()
            logger.info(f"User exists check for {email}: {user_exists}")
        except Exception as e:
            logger.error(f"Error checking user existence: {str(e)}")
        
        # Use authenticate() with proper parameters for custom User model
        request = self.context.get('request')
        logger.info(f"Attempting authentication for {email}")
        user = authenticate(request=request, username=email, password=password)
        
        logger.info(f"Authentication result for {email}: {user}")
        
        if not user:
            logger.error(f"Authentication failed for {email}")
            raise serializers.ValidationError('Invalid email or password')
        
        if not user.is_active:
            logger.error(f"User {email} is not active")
            raise serializers.ValidationError('Account is disabled')
        
        logger.info(f"Authentication successful for {email}")
        attrs['user'] = user
        return attrs


class GoogleLoginSerializer(serializers.Serializer):
    """Simplified Google login using django-allauth integration"""
    access_token = serializers.CharField()
    
    def validate(self, attrs):
        access_token = attrs.get('access_token')
        
        if not access_token:
            raise serializers.ValidationError('Google access token is required')
        
        try:
            # Use Google userinfo endpoint to get user data
            import requests
            response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=10
            )
            
            if response.status_code == 401:
                raise serializers.ValidationError('Invalid or expired Google token')
            elif response.status_code != 200:
                raise serializers.ValidationError('Failed to verify Google token')
            
            google_data = response.json()
            
            # Extract user information
            email = google_data.get('email')
            first_name = google_data.get('given_name', '').strip()
            last_name = google_data.get('family_name', '').strip()
            
            if not email:
                raise serializers.ValidationError('Email not provided by Google')
            
            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name or 'User',
                    'last_name': last_name or '',
                    'email_verified': True,
                    'user_type': 'customer'
                }
            )
            
            # Update existing user info if needed
            if not created and not user.email_verified:
                user.email_verified = True
                user.save(update_fields=['email_verified'])
            
            attrs['user'] = user
            
        except requests.exceptions.RequestException:
            raise serializers.ValidationError('Unable to connect to Google services')
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Google OAuth error: {str(e)}', exc_info=True)
            raise serializers.ValidationError('Google authentication failed')
        
        return attrs


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    plan_id = serializers.UUIDField(write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'plan_id', 'status', 'is_active',
                 'trial_end', 'current_period_start', 'current_period_end',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Invalid password')
        return value


class GoogleCallbackSerializer(serializers.Serializer):
    """Serializer for Google OAuth2 callback with authorization code"""
    code = serializers.CharField(help_text="Authorization code from Google")
    state = serializers.CharField(required=False, help_text="CSRF state parameter")
    
    def validate_code(self, value):
        if not value:
            raise serializers.ValidationError('Authorization code is required')
        return value