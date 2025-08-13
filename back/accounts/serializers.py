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
                 'user_type', 'email_verified', 'date_joined']
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
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('Account is disabled')
        else:
            raise serializers.ValidationError('Email and password are required')
        
        attrs['user'] = user
        return attrs


class GoogleLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    
    def validate(self, attrs):
        access_token = attrs.get('access_token')
        
        if not access_token:
            raise serializers.ValidationError({
                'access_token': 'Google access token is required'
            })
        
        try:
            # Handle different token types with better error handling
            google_data = self._verify_google_token(access_token)
            
            # Extract user information
            email = google_data.get('email')
            first_name = google_data.get('given_name', '').strip()
            last_name = google_data.get('family_name', '').strip()
            email_verified = google_data.get('email_verified', False)
            
            # Validate email
            if not email:
                raise serializers.ValidationError({
                    'email': 'Email address not provided by Google'
                })
            
            if not email_verified:
                raise serializers.ValidationError({
                    'email': 'Email address not verified by Google'
                })
            
            # Get or create user with better error handling
            user = self._get_or_create_user(email, first_name, last_name)
            
            attrs['user'] = user
            attrs['google_data'] = google_data
            
        except serializers.ValidationError:
            raise
        except requests.exceptions.Timeout:
            raise serializers.ValidationError({
                'network': 'Google authentication timed out. Please try again.'
            })
        except requests.exceptions.ConnectionError:
            raise serializers.ValidationError({
                'network': 'Unable to connect to Google services. Please check your connection.'
            })
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError({
                'network': f'Network error during Google authentication: {str(e)}'
            })
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Unexpected error in Google OAuth: {str(e)}', exc_info=True)
            raise serializers.ValidationError({
                'unknown': 'An unexpected error occurred during Google authentication'
            })
        
        return attrs
    
    def _verify_google_token(self, access_token):
        """Verify Google token and return user data"""
        if access_token.startswith('eyJ'):
            # JWT token - verify with Google's public keys
            return self._verify_jwt_token(access_token)
        else:
            # Access token - verify with Google userinfo endpoint
            return self._verify_access_token(access_token)
    
    def _verify_jwt_token(self, jwt_token):
        """Verify JWT token with Google's public keys"""
        import jwt
        from jwt.algorithms import RSAAlgorithm
        import requests
        
        try:
            # Get Google's public keys with timeout
            jwks_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/certs',
                timeout=10
            )
            
            if jwks_response.status_code != 200:
                raise serializers.ValidationError({
                    'token': 'Unable to verify token with Google'
                })
            
            jwks = jwks_response.json()
            
            # Decode token header to get the key ID
            try:
                unverified_header = jwt.get_unverified_header(jwt_token)
            except jwt.DecodeError:
                raise serializers.ValidationError({
                    'token': 'Invalid JWT token format'
                })
            
            # Find the correct key
            rsa_key = None
            for key in jwks.get('keys', []):
                if key.get('kid') == unverified_header.get('kid'):
                    rsa_key = {
                        'kty': key.get('kty'),
                        'kid': key.get('kid'),
                        'use': key.get('use'),
                        'n': key.get('n'),
                        'e': key.get('e')
                    }
                    break
            
            if not rsa_key:
                raise serializers.ValidationError({
                    'token': 'Unable to find matching verification key'
                })
            
            # Verify and decode token
            try:
                public_key = RSAAlgorithm.from_jwk(rsa_key)
                client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
                
                if not client_id:
                    raise serializers.ValidationError({
                        'configuration': 'Google Client ID not configured'
                    })
                
                payload = jwt.decode(
                    jwt_token,
                    public_key,
                    algorithms=['RS256'],
                    audience=client_id,
                    issuer=['https://accounts.google.com', 'accounts.google.com']
                )
                
                return {
                    'email': payload.get('email'),
                    'given_name': payload.get('given_name', ''),
                    'family_name': payload.get('family_name', ''),
                    'picture': payload.get('picture', ''),
                    'email_verified': payload.get('email_verified', False)
                }
                
            except jwt.ExpiredSignatureError:
                raise serializers.ValidationError({
                    'token': 'Google token has expired. Please sign in again.'
                })
            except jwt.InvalidAudienceError:
                raise serializers.ValidationError({
                    'token': 'Invalid token audience'
                })
            except jwt.InvalidIssuerError:
                raise serializers.ValidationError({
                    'token': 'Invalid token issuer'
                })
            except jwt.InvalidTokenError as e:
                raise serializers.ValidationError({
                    'token': f'Invalid JWT token: {str(e)}'
                })
                
        except requests.exceptions.RequestException:
            raise serializers.ValidationError({
                'token': 'Unable to verify token with Google servers'
            })
    
    def _verify_access_token(self, access_token):
        """Verify access token with Google userinfo endpoint"""
        import requests
        
        try:
            response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=10
            )
            
            if response.status_code == 401:
                raise serializers.ValidationError({
                    'token': 'Invalid or expired Google access token'
                })
            elif response.status_code != 200:
                raise serializers.ValidationError({
                    'token': f'Google API error (status: {response.status_code})'
                })
            
            return response.json()
            
        except requests.exceptions.RequestException:
            raise serializers.ValidationError({
                'token': 'Unable to verify access token with Google'
            })
    
    def _get_or_create_user(self, email, first_name, last_name):
        """Get existing user or create new one"""
        try:
            user = User.objects.get(email=email)
            
            # Update user info if needed and user hasn't set custom info
            updated_fields = []
            if not user.first_name and first_name:
                user.first_name = first_name
                updated_fields.append('first_name')
            if not user.last_name and last_name:
                user.last_name = last_name
                updated_fields.append('last_name')
            if not user.email_verified:
                user.email_verified = True
                updated_fields.append('email_verified')
            
            if updated_fields:
                user.save(update_fields=updated_fields)
                
            return user
            
        except User.DoesNotExist:
            # Create new user
            try:
                user = User.objects.create_user(
                    email=email,
                    first_name=first_name or 'User',
                    last_name=last_name or '',
                    email_verified=True,
                    user_type='customer'
                )
                return user
                
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Failed to create user {email}: {str(e)}', exc_info=True)
                raise serializers.ValidationError({
                    'user_creation': 'Failed to create user account'
                })


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