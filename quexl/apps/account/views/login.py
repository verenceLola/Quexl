from django.utils.timezone import now
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from quexl.apps.account.backends import JWTAuthentication
from quexl.apps.account.models import User
from quexl.apps.account.renderers import UserJSONRenderer
from quexl.apps.account.serializers import LoginSerializer


class LoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    operation = "Login"
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        """Login a user"""
        email, password = (
            request.data.get("email", None),
            request.data.get("password", None),
        )

        user = {"email": email, "password": password}
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.data

        user = User.get_user(user_data["email"])
        userdata = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
        }
        token = JWTAuthentication.generate_token(userdata=userdata)
        # update user last login
        user.last_login = now()
        user.save()

        return Response(
            {
                "message": "You have successfully logged in",
                "meta": {"token": token},
            },
            status=status.HTTP_200_OK,
        )
