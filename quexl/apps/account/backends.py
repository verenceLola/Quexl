"""Configure JWT Here"""

import datetime
import logging

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

"""Configure JWT Here"""

# Get an instance of a logger
logger = logging.getLogger(__name__)


class JWTAuthentication(TokenAuthentication):
    """Inherit the JSON web authentication class from rest_framework_jwt"""

    keyword = "Bearer"

    @staticmethod
    def generate_token(userdata):
        secret = settings.SECRET_KEY
        token = jwt.encode(
            {
                "userdata": userdata,
                "iat": datetime.datetime.utcnow(),
                "nbf": datetime.datetime.utcnow()
                + datetime.timedelta(minutes=-5),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            },
            secret,
        )
        # decode the byte type token to
        token = token.decode("utf-8")

        return token

    @staticmethod
    def decode_jwt(token):
        """ Method for decoding token."""
        # It takes the token, secret_key and algorithm
        user_details = jwt.decode(
            token, settings.SECRET_KEY, algorithm="HS256"
        )

        return user_details

    def authenticate_credentials(self, key):
        try:
            # decode the payload and get the user
            payload = jwt.decode(key, settings.SECRET_KEY)
            user = get_user_model().objects.get(
                username=payload["userdata"]["username"]
            )  # noqa E501
        except (jwt.DecodeError, get_user_model().DoesNotExist):
            raise exceptions.AuthenticationFailed("Invalid token")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User inactive or deleted")

        return user, payload

    @staticmethod
    def generate_reset_token(email):
        """ generates reset password token """

        token = jwt.encode(
            {
                "email": email,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(minutes=720),
                "jti": settings.SECRET_KEY,
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        ).decode()

        return token


class TokenGenerator(PasswordResetTokenGenerator):
    @staticmethod
    def _generate_hash_value(user, timestamp):

        return (
            six.text_type(user.email)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
