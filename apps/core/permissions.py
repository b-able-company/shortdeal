"""
Custom permission classes for ShortDeal API
"""
from rest_framework import permissions


class IsProducer(permissions.BasePermission):
    """Permission for producer (creator) users only"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'creator'


class IsBuyer(permissions.BasePermission):
    """Permission for buyer users only"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'buyer'


class IsAdmin(permissions.BasePermission):
    """Permission for admin users only"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsOwner(permissions.BasePermission):
    """Permission to only allow owners of an object to access it"""

    def has_object_permission(self, request, view, obj):
        # Check if object has user/owner field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'producer'):
            return obj.producer == request.user
        if hasattr(obj, 'buyer'):
            return obj.buyer == request.user
        return False


class IsRelatedParty(permissions.BasePermission):
    """Permission for parties related to an offer/LOI (producer or buyer)"""

    def has_object_permission(self, request, view, obj):
        user = request.user
        # For Offer and LOI models
        if hasattr(obj, 'content') and hasattr(obj.content, 'producer'):
            return user == obj.content.producer or user == obj.buyer
        # Direct producer/buyer check
        if hasattr(obj, 'producer') and hasattr(obj, 'buyer'):
            return user == obj.producer or user == obj.buyer
        return False


class IsOnboarded(permissions.BasePermission):
    """Permission to check if user has completed onboarding"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_onboarded

    message = "You must complete onboarding before accessing this resource."
