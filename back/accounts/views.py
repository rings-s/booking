# accounts/views.py
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from datetime import timedelta
import logging
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    GoogleLoginSerializer, SubscriptionSerializer,
    SubscriptionPlanSerializer, ChangePasswordSerializer
)
from .models import Subscription, SubscriptionPlan
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create free subscription
        free_plan = SubscriptionPlan.objects.get(name='free')
        Subscription.objects.create(
            user=user,
            plan=free_plan,
            status='active',
            current_period_start=timezone.now(),
            current_period_end=timezone.now() + timedelta(days=30)
        )
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"Login attempt with data: {request.data}")
            serializer = self.get_serializer(data=request.data)
            
            if not serializer.is_valid():
                logger.error(f"Serializer errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.validated_data['user']
            logger.info(f"User authenticated: {user.email}")
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Login failed', 'detail': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class GoogleLoginView(generics.GenericAPIView):
    serializer_class = GoogleLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Ensure user has a subscription
        self._ensure_user_subscription(user)
        
        # Generate JWT tokens (consistent with LoginView)
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
        
        # Add security headers to response
        response = Response(response_data, status=status.HTTP_200_OK)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _ensure_user_subscription(self, user):
        """Ensure user has a subscription, create free one if needed"""
        subscription_created = False
        
        if not hasattr(user, 'subscription'):
            try:
                free_plan, plan_created = SubscriptionPlan.objects.get_or_create(
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
                
                Subscription.objects.create(
                    user=user,
                    plan=free_plan,
                    status='active',
                    current_period_start=timezone.now(),
                    current_period_end=timezone.now() + timedelta(days=30)
                )
                subscription_created = True
                
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Failed to create subscription for user {user.email}: {str(e)}', exc_info=True)
                # Don't fail the login if subscription creation fails
                pass
        
        return subscription_created


class GoogleCallbackView(generics.GenericAPIView):
    """Handle Google OAuth2 authorization code callback"""
    permission_classes = [AllowAny]
    throttle_scope = 'oauth_callback'
    
    def post(self, request, *args, **kwargs):
        import logging
        import requests
        from django.conf import settings
        
        logger = logging.getLogger(__name__)
        client_ip = self.get_client_ip(request)
        
        try:
            # Get authorization code from request
            auth_code = request.data.get('code')
            if not auth_code:
                return Response({
                    'error': 'Authorization code is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Exchange authorization code for access token
            token_data = self._exchange_code_for_token(auth_code)
            
            # Get user info using access token
            user_info = self._get_user_info(token_data['access_token'])
            
            # Create or get user
            user = self._get_or_create_user_from_info(user_info)
            
            # Ensure user has subscription
            subscription_created = self._ensure_user_subscription(user)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            # Add custom claims
            access_token['login_method'] = 'google_callback'
            access_token['ip'] = client_ip
            
            logger.info(f'Google OAuth callback successful for user: {user.email} from IP: {client_ip}')
            
            response_data = {
                'user': UserSerializer(user).data,
                'access': str(access_token),
                'refresh': str(refresh),
                'subscription_created': subscription_created
            }
            
            response = Response(response_data, status=status.HTTP_200_OK)
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['X-XSS-Protection'] = '1; mode=block'
            
            return response
            
        except Exception as e:
            logger.error(f'Google OAuth callback error from IP: {client_ip}: {str(e)}', exc_info=True)
            return Response({
                'error': 'Authentication failed',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _exchange_code_for_token(self, auth_code):
        """Exchange authorization code for access token"""
        import requests
        from django.conf import settings
        
        token_url = 'https://oauth2.googleapis.com/token'
        
        # Get client credentials from settings
        client_id = getattr(settings, 'GOOGLE_CLIENT_ID', None)
        client_secret = getattr(settings, 'GOOGLE_CLIENT_SECRET', None)
        
        if not client_id or not client_secret:
            raise Exception('Google OAuth credentials not configured')
        
        token_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code',
            'redirect_uri': f'{settings.FRONTEND_URL}/auth/google/callback'
        }
        
        try:
            response = requests.post(token_url, data=token_data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f'Failed to exchange code for token: {str(e)}')
    
    def _get_user_info(self, access_token):
        """Get user information using access token"""
        import requests
        
        try:
            response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f'Failed to get user info: {str(e)}')
    
    def _get_or_create_user_from_info(self, user_info):
        """Create or get user from Google user info"""
        email = user_info.get('email')
        first_name = user_info.get('given_name', '').strip()
        last_name = user_info.get('family_name', '').strip()
        email_verified = user_info.get('verified_email', False)
        
        if not email:
            raise Exception('Email not provided by Google')
        
        if not email_verified:
            raise Exception('Email not verified by Google')
        
        try:
            user = User.objects.get(email=email)
            
            # Update user info if needed
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
            user = User.objects.create_user(
                email=email,
                first_name=first_name or 'User',
                last_name=last_name or '',
                email_verified=True,
                user_type='customer'
            )
            return user
    
    def _ensure_user_subscription(self, user):
        """Ensure user has a subscription, create free one if needed"""
        subscription_created = False
        
        if not hasattr(user, 'subscription'):
            try:
                free_plan, plan_created = SubscriptionPlan.objects.get_or_create(
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
                
                Subscription.objects.create(
                    user=user,
                    plan=free_plan,
                    status='active',
                    current_period_start=timezone.now(),
                    current_period_end=timezone.now() + timedelta(days=30)
                )
                subscription_created = True
                
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Failed to create subscription for user {user.email}: {str(e)}', exc_info=True)
                # Don't fail the login if subscription creation fails
                pass
        
        return subscription_created


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({'message': 'Password changed successfully'})


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [AllowAny]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def upgrade(self, request):
        plan_id = request.data.get('plan_id')
        # Stripe integration for subscription upgrade
        return Response({'message': 'Subscription upgrade implementation'})
    
    @action(detail=False, methods=['get'])
    def usage(self, request):
        """
        Get usage statistics for the user's current subscription
        """
        try:
            subscription = Subscription.objects.get(
                user=request.user,
                status='active'
            )
            
            # Calculate usage statistics
            usage_data = {
                'plan_name': subscription.plan.name,
                'current_period_start': subscription.current_period_start,
                'current_period_end': subscription.current_period_end,
                'businesses_used': subscription.user.owned_businesses.filter(is_active=True).count(),
                'businesses_limit': subscription.plan.max_businesses,
                'bookings_this_month': 0,  # Calculate from bookings
                'bookings_limit': subscription.plan.max_bookings_per_month,
                'storage_used': 0,  # Calculate from file uploads
                'storage_limit': subscription.plan.max_storage_gb,
            }
            
            return Response(usage_data)
        except Subscription.DoesNotExist:
            return Response(
                {'error': 'No active subscription found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def invoices(self, request):
        """
        Get billing history and invoices for the user
        """
        try:
            subscription = Subscription.objects.get(
                user=request.user,
                status='active'
            )
            
            # Mock invoice data - in production this would come from Stripe
            invoices_data = [
                {
                    'id': 'inv_001',
                    'date': subscription.current_period_start,
                    'amount': float(subscription.plan.price),
                    'status': 'paid',
                    'plan_name': subscription.plan.name,
                    'period_start': subscription.current_period_start,
                    'period_end': subscription.current_period_end,
                    'download_url': None  # Would be Stripe invoice URL
                }
            ]
            
            return Response(invoices_data)
        except Subscription.DoesNotExist:
            return Response(
                {'error': 'No active subscription found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a subscription
        """
        try:
            subscription = self.get_object()
            if subscription.user != request.user:
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            subscription.status = 'cancelled'
            subscription.cancelled_at = timezone.now()
            subscription.save()
            
            serializer = self.get_serializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response(
                {'error': 'Subscription not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        """
        Resume a cancelled subscription
        """
        try:
            subscription = self.get_object()
            if subscription.user != request.user:
                return Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if subscription.status == 'cancelled':
                subscription.status = 'active'
                subscription.cancelled_at = None
                subscription.save()
                
                serializer = self.get_serializer(subscription)
                return Response(serializer.data)
            else:
                return Response(
                    {'error': 'Subscription is not cancelled'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Subscription.DoesNotExist:
            return Response(
                {'error': 'Subscription not found'},
                status=status.HTTP_404_NOT_FOUND
            )