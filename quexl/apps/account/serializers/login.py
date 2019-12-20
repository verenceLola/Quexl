from django.contrib.auth import authenticate
from rest_framework import serializers

from ..backends import JWTAuthentication
from ..models import User


class LoginSerializer(serializers.Serializer):
    """The class to serialize login details"""

    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        """
        validate details
        """
        user = data.get("email", None)  # get user object as key 'email'
        email = user.email
        password = data.get("password", None)

        if not password:
            raise serializers.ValidationError(
                "Kindly enter your password to log in."
            )
        auth_user = authenticate(email=email, password=password)

        if not user.is_active:
            raise serializers.ValidationError(
                "Your account is inactive. Kindly check your email for an "
                "activation link to activate "
            )

        if auth_user is None:
            raise serializers.ValidationError(
                {
                    "password": "Password isn’t right. Double check "
                    ", or reset your password to log in. "
                }
            )
        token = JWTAuthentication.generate_token(email)

        return {"email": user.email, "username": user.username, "token": token}

    def validate_email(self, value):
        """
        validate user password
        """
        user = User.get_user(value)

        if not user:
            raise serializers.ValidationError(
                f"User with email {value} not found."
            )

        return user  # return user object to reduce unnecessary db queries
