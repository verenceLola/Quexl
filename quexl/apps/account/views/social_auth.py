from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from social_core.exceptions import MissingBackend
from social_django.utils import load_strategy

from quexl.apps.account.backends import JWTAuthentication
from quexl.apps.account.serializers import SocialAuthSerializer
from quexl.utils.social_auth import SocialAuth


class SocialAuthView(GenericAPIView):
    """Authenticate via social sites (Google & Facebook)"""

    permission_classes = (AllowAny,)
    serializer_class = SocialAuthSerializer
    operation = "Social authentication"

    def post(self, request, *args, **kwargs):
        """Takes in provider and access_token to authenticate user"""
        serializer = self.serializer_class(data=request.data["authData"])
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get("provider")
        strategy = load_strategy(request)
        social_auth = SocialAuth(request, provider, strategy)
        try:
            access_token = social_auth.get_access_token(
                request.data, serializer.data
            )

        except MissingBackend:

            return Response(
                {"error": "The Provider is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except APIException as e:
            return Response({"error": e.detail}, status=e.status_code)
        # Go through the pipeline to create user if they don't exist
        try:
            user = social_auth.save_user(access_token)

        except BaseException:

            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        userdata = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
        }
        token = JWTAuthentication.generate_token(userdata=userdata)

        return Response(
            {"message": "You have successfully logged in.", "token": token},
            status=status.HTTP_200_OK,
        )
