from urllib.parse import quote
from urllib.parse import urlencode

import pytest
from django.contrib.auth.models import AnonymousUser

from ..middlewares import JWTAuthMiddleware

JWT = JWTAuthMiddleware({})


def test_jwt_auth_middleware_using_valid_header_token(
    generate_access_token1, mocker
):
    """
    test auth jwt token middleware using valid header token
    """
    token, user = generate_access_token1
    mocker.patch.object(JWT, "inner")
    headers = [(b"authorization", f"Bearer {token}".encode())]
    JWT(scope={"headers": headers, "query_string": b""})
    JWT.inner.assert_called_once_with(
        {"headers": headers, "query_string": b"", "user": user}
    )


def test_jwt_auth_middleware_using_valid_query_string_token(
    generate_access_token1, mocker
):
    """
    test auth jwt mtoken middleware using valid query string token
    """
    token, user = generate_access_token1
    mocker.patch.object(JWT, "inner")
    query_string = urlencode(
        {"token": f"Bearer {token}"}, quote_via=quote
    ).encode()
    JWT(scope={"query_string": query_string, "headers": []})
    JWT.inner.assert_called_once_with(
        {"query_string": query_string, "headers": [], "user": user}
    )


@pytest.mark.parametrize(
    "token", [("invalid%$token",), ("invalid formed token",)]
)
def test_auth_middleware_with_invalid_token(mocker, token):
    """
    test auth middleware with invalid token
    """
    user = AnonymousUser()
    mocker.patch.object(JWT, "inner")
    headers = [(b"authorization", f"Bearer {token}".encode())]
    JWT(scope={"headers": headers, "query_string": b""})
    JWT.inner.assert_called_once_with(
        {
            "headers": headers,
            "query_string": b"",
            "user": user,
            "error": "Invalid token",
        }
    )


def test_auth_without_authentication(mocker):
    """
    test auth middleware without authentication credentials
    """
    user = AnonymousUser()
    mocker.patch.object(JWT, "inner")
    JWT(scope={"headers": [], "query_string": b""})
    JWT.inner.assert_called_once_with(
        {
            "headers": [],
            "query_string": b"",
            "user": user,
            "error": "Authentication credentials not provided",
        }
    )
