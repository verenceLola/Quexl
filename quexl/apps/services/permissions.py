"""
custom permissions for services view
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    ensure the user is owner or performing read-only request
    """

    def has_object_permission(self, request, view, obj):
        import pdb

        pdb.set_trace()
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user


class IsSellerOrBuyer(permissions.BasePermission):
    """
    esure user is either the seller or a buyer for a given payment
    """

    def has_object_permission(self, request, view, obj):
        import pdb

        pdb.set_trace()
        return (request.user != obj.buyer) or (request.user != obj.seller)
