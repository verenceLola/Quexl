"""
configure common methods for websocket testing
"""
import json
import re
from contextlib import asynccontextmanager

import pytest
from channels.testing import WebsocketCommunicator
from rest_framework.exceptions import AuthenticationFailed

from quexl.apps.messaging.consumers import BroadcastChatConsumer
from quexl.apps.messaging.consumers import DMChatConsumer
from quexl.apps.messaging.consumers import GroupChatConsumer
from quexl.apps.messaging.models import Thread
from quexl.utils.tests.mock_websocket_auth import MockWebSocketAuth

ENDPOINTS = {
    "/chat/dm/": DMChatConsumer,
    "/chat/group/": GroupChatConsumer,
    "/chat/broadcast/": BroadcastChatConsumer,
}


def match_endpoint(endpoint):
    """
    match websocket endpoints
    """
    return re.search(r"\/chat\/\w+\/", endpoint).group()


@pytest.fixture()
def websocket_connection(monkeypatch):
    @asynccontextmanager
    async def _websocket_connection(*args, **kwargs):
        ws_endpoint = kwargs.get("endpoint")
        access_token = kwargs.get("access_token")
        monkeypatch.setattr(
            ENDPOINTS.get(match_endpoint(ws_endpoint)),
            "connect",
            lambda x: MockWebSocketAuth.connect(x),
        )
        comm = WebsocketCommunicator(
            ENDPOINTS.get(match_endpoint(ws_endpoint)),
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
def websocket_send_message(websocket_connection):
    """
    pytest fixture for sending websocket message
    """

    async def _websocket_send_message(**kwargs):
        token = kwargs.pop("token")
        endpoint = kwargs.pop("endpoint")
        ws_msg = json.dumps(kwargs)
        async with websocket_connection(
            endpoint=endpoint, access_token=token
        ) as ws:
            await ws.send_to(text_data=ws_msg)
            response = await ws.receive_json_from()

        return response

    return _websocket_send_message


@pytest.fixture()
def create_user_group(generate_access_token1, django_user_model):
    """
    pytest fixture to create and add user to chat group
    """

    @pytest.mark.django_db(transaction=True)
    def _create_user_group(*args, **kwargs):
        token, user = generate_access_token1
        group_name = kwargs.get("group_name")
        members = kwargs.get("members")
        assert isinstance(members, list)
        participants = [
            django_user_model.objects.create(
                username=y, password="pass1234", email=f"{y}@quexl.com"
            )
            for y in members
        ]
        participants.append(user)  # add current user to created group
        group = Thread.objects.create(name=group_name, type="group")
        group.participants.set(participants)
        assert group.participants.count() == len(members) + 1

        return group_name

    return _create_user_group
