from rest_framework import serializers

from ..models import User


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for forget password"""

    email = serializers.CharField(max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for reset password"""

    class Meta:
        model = User
        fields = ("password",)
