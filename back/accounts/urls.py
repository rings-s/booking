# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenObtainPairView, TokenVerifyView
)
from .views import (
    RegisterView, LoginView, GoogleLoginView, GoogleCallbackView,
    UserViewSet, SubscriptionPlanViewSet, SubscriptionViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'plans', SubscriptionPlanViewSet)
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    # JWT Token endpoints (djangorestframework-simplejwt)
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Custom auth endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('google-callback/', GoogleCallbackView.as_view(), name='google-callback'),
    
    # ViewSets
    path('', include(router.urls)),
]