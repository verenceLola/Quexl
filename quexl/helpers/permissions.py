"""
custom permissions for services and orders view
"""
from rest_framework import permissions


class IsSellerOrReadOnly(permissions.BasePermission):
    """
    ensure the user is owner or performing read-only request
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.seller


class IsBuyerOrReadOnly(permissions.BasePermission):
    """
    ensure the user is buyer or performing read-only request
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.buyer


class IsBuyerOrSeller(permissions.BasePermission):
    """
    ensure the user is seller
    """

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
        ):  # allow buyers or sellers to view orders made
            return (request.user == obj.buyer) or (request.user == obj.seller)
        return request.user == obj.buyer
