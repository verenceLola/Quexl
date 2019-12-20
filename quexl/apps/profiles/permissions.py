from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    ensure user is onwer or read-only access
    """

    def has_object_permission(self, request, view, obj):
        """
        ensure request is readonly and owner can edit
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.user
