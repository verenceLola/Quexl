import jwt
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from quexl.apps.account.backends import JWTAuthentication
from quexl.apps.account.models import User


class UserActivationAPIView(GenericAPIView):
    """Activate a user after mail verification."""

    permission_classes = (AllowAny,)
    operation = "Account activation"

    def get(self, request, token, *args, **kwargs):
        """ Method for getting user token and activating them. """

        try:
            data = JWTAuthentication.decode_jwt(token)
            user = User.objects.get(username=data["userdata"]["username"])
        except (User.DoesNotExist, jwt.exceptions.DecodeError):

            return Response(
                {"message": "Activation link is invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_active = True
        user.save()

        return Response(
            {"message": "Account activated successfully."},
            status=status.HTTP_200_OK,
        )
