from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from quexl.apps.account.email import Email
from quexl.apps.account.renderers import UserJSONRenderer
from quexl.apps.account.serializers import RegistrationSerializer


class SignUpAPIView(GenericAPIView):
    """Register a new user"""

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer
    operation = "Signup"

    def post(self, request: Request, **kwargs) -> Response:
        """ Signup a new user """
        email, username, password = (
            request.data.get("email", None),
            request.data.get("username", None),
            request.data.get("password", None),
        )

        user = {"email": email, "username": username, "password": password}

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        Email.send_email(request, user)
        serializer.save()

        return Response(
            {
                "message": "Please confirm your Quexl account by clicking on the "
                "link sent to your email account {}".format(email)
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request: Request) -> Response:

        return Response(
            {"message": "Only POST requests are allowed to this endpoint."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
