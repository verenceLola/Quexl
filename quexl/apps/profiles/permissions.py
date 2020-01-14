from rest_framework import permissions
from rest_framework.request import Request

from quexl.apps.profiles.models import Profile


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    ensure user is onwer or read-only access
    """

    def has_object_permission(
        self, request: Request, view, obj: Profile
    ) -> bool:
        """
        ensure request is readonly and owner can edit
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.user
