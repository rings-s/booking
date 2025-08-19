# accounts/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class IsBusinessOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'business_owner' or request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_superuser


class HasActiveSubscription(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if hasattr(request.user, 'subscription'):
            return request.user.subscription.is_active
        return False


class CanCreateBooking(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.user_type in ['customer', 'admin']