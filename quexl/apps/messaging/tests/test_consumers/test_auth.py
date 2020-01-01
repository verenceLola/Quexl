import pytest
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed


@pytest.mark.asyncio
async def test_auth_using_header_token(
    websocket_connection, generate_access_token1
):
    token, user = generate_access_token1
    async with websocket_connection(
        endpoint="/chat/dm/", access_token=token
    ) as ws:
        assert ws.scope["user"] == user


@pytest.mark.asyncio
async def test_auth_using_query_param(
    websocket_connection, generate_access_token1
):
    token, user = generate_access_token1
    async with websocket_connection(
        endpoint=f"/chat/dm/?token=Bearer {token}"
    ) as ws:
        assert ws.scope["user"] == user


@pytest.mark.asyncio
async def test_auth_with_invalid_token(websocket_connection):
    invalid_token = "invalid&%%$token"
    with pytest.raises(
        AuthenticationFailed, match="WebSocket connection failed"
    ):
        async with websocket_connection(
            endpoint="/chat/dm/", access_token=invalid_token
        ) as ws:
            assert ws.scope["user"] == AnonymousUser
