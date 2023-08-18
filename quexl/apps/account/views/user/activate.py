from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from quexl.apps.account.models import User


class ActivateUserAPIView(GenericAPIView):
    """Activate a deactivated account acount"""

    permission_classes = (IsAdminUser,)
    operation = "Account activation"

    def get(self, request, *args, **kwargs):
        """Method for activating user acount"""
        user = User.objects.get(id=kwargs.get("id"))
        if user.is_active:
            return Response(
                {"message": "Account activated successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            user.is_active = True
            user.save()
            return Response(
                {"message": "Account activated successfully."},
                status=status.HTTP_200_OK,
            )
