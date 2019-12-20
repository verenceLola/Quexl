from rest_framework import status
from rest_framework.exceptions import APIException
from social_core.backends.oauth import BaseOAuth1
from social_core.backends.oauth import BaseOAuth2
from social_django.utils import load_backend

from quexl.apps.account.models import User


class SocialAuth:
    """
    social auth helper functions
    """

    def __init__(self, request, provider, strategy):
        self.provider = provider
        self.strategy = strategy
        self.request = request

    def get_access_token(self, serializer_data) -> str:
        """
        get access_token from social auth provider
        """
        access_token = None
        self.backend = load_backend(
            strategy=self.strategy, name=self.provider, redirect_uri=None
        )

        if isinstance(self.backend, BaseOAuth1):
            if "access_token_secret" in self.request.data:
                access_token = {
                    "oauth_token": self.request.data["access_token"],
                    "oauth_token_secret": self.request.data[
                        "access_token_secret"
                    ],
                }
            else:
                raise APIException(
                    detail="Access token secret is required",
                    code=status.HTTP_400_BAD_REQUEST,
                )

        elif isinstance(self.backend, BaseOAuth2):

            access_token = serializer_data.get("access_token")

        return access_token

    def save_user(self, access_token, **kwargs) -> User:
        """
        save user if not in db
        """
        request = self.request
        authenticated_user = (
            request.user if not request.user.is_anonymous else None
        )
        user = self.backend.do_auth(access_token, user=authenticated_user)
        user.is_active = True
        user.save()
        return user
