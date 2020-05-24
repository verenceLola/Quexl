from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from quexl.apps.account.models import User


class DeactivateUserAPIView(GenericAPIView):
    """Deactivate user acount"""

    permission_classes = (IsAuthenticated,)
    operation = "Account deactivation"

    def get(self, request, *args, **kwargs):
        """ Method for deactivating user acount"""
        user = User.objects.get(id=kwargs.get("id"))
        if request.user == user or request.user.is_superuser:
            user.is_active = False
            user.save()

            return Response(
                {"message": "Account deactivated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"Error": "Could not perform this action"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
