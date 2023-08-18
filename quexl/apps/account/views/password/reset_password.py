import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from quexl.apps.account.models import User
from quexl.apps.account.serializers import ResetPasswordSerializer


class ResetPasswordView(GenericAPIView):
    # This is the view that changes the password.
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer
    operation = "Password reset"

    def put(self, request: Request, token: str, *args, **kwargs) -> Response:
        try:
            new_password = request.data.get("password")
            serializer = self.serializer_class(data={"password": new_password})
            serializer.is_valid(raise_exception=True)
            decode_token = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256"
            )
            email = decode_token.get("email")
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            return Response(
                {"message": "Your password has been successfully changed"},
                status=status.HTTP_200_OK,
            )
        except jwt.PyJWTError:
            return Response(
                {
                    "error": "Invalid token. Please request a new password reset "
                    "link."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
