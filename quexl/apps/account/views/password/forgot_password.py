import datetime

import furl
import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from quexl.apps.account.models import User
from quexl.apps.account.serializers import ForgotPasswordSerializer


class ForgotPasswordView(GenericAPIView):
    # This view handles sending the password reset request email.
    # We expect the user to enter an email that exists in the database
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request: Request) -> Response:
        """User Forgot Password"""

        try:
            requester_data = request.data.get("email")
            user = User.objects.get(email=requester_data)

            # Get URL for client and include in the email for password reset
            subject = "Password Reset - Quexl"
            message = "Reset your password "

            # generate token token that expires after 24 hours
            token = jwt.encode(
                {
                    "email": user.email,
                    "iat": datetime.datetime.now(),
                    "exp": datetime.datetime.utcnow()
                    + datetime.timedelta(hours=24),
                },
                settings.SECRET_KEY,
                algorithm="HS256",
            ).decode()

            # format url and send it in the reset email link

            # TODO: Configure link to referer upon password reset
            client_url = request.META.get(
                "HTTP_REFERER", request.build_absolute_uri("/").strip("/")
            )
            reset_link_url = furl.furl(client_url)
            reset_link_url.args = (("token", token),)

            body = render_to_string(
                "reset_password.html",
                {"link": reset_link_url, "name": user.username},
            )

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                html_message=body,
                fail_silently=True,
            )

            return Response(
                {
                    "message": "An email has been sent to your inbox with a "
                    "password reset link."
                },
                status=status.HTTP_200_OK,
            )

        except (KeyError, User.DoesNotExist):
            return Response(
                {
                    "message": "Password Reset Request failed",
                    "error": "Missing or non-existing email.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
