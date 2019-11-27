from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework.exceptions import AuthenticationFailed

from quexl.apps.account.backends import JWTAuthentication


class JWTAuthMiddleware:
    """
    JWT auth middleware for Django Channels
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope["headers"])
        query_string = scope["query_string"]

        if b"token" in query_string:
            parsed_query_string = parse_qs(query_string)
            headers.update(
                {b"authorization": parsed_query_string[b"token"][0]}
            )

        if b"authorization" in headers:
            try:
                token_name, token_value = (
                    headers[b"authorization"].decode().split()
                )
                if token_name == "Bearer":
                    user, _ = JWTAuthentication().authenticate_credentials(
                        token_value
                    )
                    scope["user"] = user
                    close_old_connections()
            except AuthenticationFailed as e:
                scope["user"] = AnonymousUser()
                scope["error"] = e.__str__()
        else:
            scope["user"] = AnonymousUser()
            scope["error"] = "Authentication credentials not provided"

        return self.inner(scope)


JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(  # noqa
    AuthMiddlewareStack(inner)
)
