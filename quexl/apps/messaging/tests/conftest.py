"""
configure common methods for websocket testing
"""
import json
from contextlib import asynccontextmanager

import pytest
from channels.testing import WebsocketCommunicator
from rest_framework.exceptions import AuthenticationFailed

from quexl.apps.messaging.consumers import DMChatConsumer
from quexl.utils.tests.mock_websocket_auth import MockWebSocketAuth


@pytest.fixture()
def websocket_connection(monkeypatch):
    @asynccontextmanager
    async def _websocket_connection(*args, **kwargs):
        ws_endpoint = kwargs.get("endpoint")
        access_token = kwargs.get("access_token")
        monkeypatch.setattr(
            DMChatConsumer, "connect", lambda x: MockWebSocketAuth.connect(x)
        )
        comm = WebsocketCommunicator(
            DMChatConsumer,
            ws_endpoint,
            headers={f"Authorization": f"Bearer {access_token}"},
        )
        try:
            connected, _ = await comm.connect()
            assert connected
            response = await comm.receive_json_from()
            assert response.get("message") == "connection established"
            yield comm
        except AssertionError:
            raise AuthenticationFailed("WebSocket connection failed")
        finally:
            await comm.disconnect()

    return _websocket_connection


@pytest.fixture()
def websocket_send_dm_message(websocket_connection):
    """
    pytest fixture for sending websocket message
    """

    async def _websocket_send_message(token, message, to):
        ws_msg = json.dumps({"to": to, "message": message})
        async with websocket_connection(
            endpoint="/chat/dm/", access_token=token
        ) as ws:
            await ws.send_to(text_data=ws_msg)
            response = await ws.receive_json_from()

        return response

    return _websocket_send_message
