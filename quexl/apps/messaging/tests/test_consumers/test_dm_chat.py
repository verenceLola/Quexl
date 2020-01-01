import pytest
from freezegun import freeze_time

from quexl.apps.messaging.models import Message
from quexl.apps.messaging.models import Thread

from .fixtures import DMMessageFixtures

fixtures = DMMessageFixtures()


@pytest.mark.asyncio
async def test_message_to_self(
    generate_access_token1, websocket_send_dm_message
):
    """
    test sending message to self
    """
    token, user = generate_access_token1
    message = "hello self"
    msg_response = await websocket_send_dm_message(
        token=token, message=message, to=user.username
    )
    assert msg_response["error"] == "You can't chat with yourself"


@pytest.mark.asyncio
async def test_sending_invalid_json_msg(
    generate_access_token1, websocket_connection
):
    """
    test sending message with invalid JSON data
    """
    token, user = generate_access_token1
    message = "invalid json data"
    async with websocket_connection(
        endpoint="/chat/dm/", access_token=token
    ) as ws:
        await ws.send_to(message)
        response = await ws.receive_json_from()
        assert response["error"] == "Invalid JSON data"


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
@freeze_time("2019-10-01")
async def test_send_msg_to_user2(
    generate_access_token1, generate_access_token2, websocket_send_dm_message
):
    """
    test sending message to known/ existing user
    """
    token1, user1 = generate_access_token1
    token2, user2 = generate_access_token2
    message1 = "hello user2!"
    message2 = "I'm fine user1"
    msg_response1 = await websocket_send_dm_message(
        token=token1, message=message1, to=user2.username
    )
    msg_response2 = await websocket_send_dm_message(
        token=token2, message=message2, to=user1.username
    )
    assert msg_response1 == DMMessageFixtures.msg_response1
    assert msg_response2 == DMMessageFixtures.msg_response2
    inbox_count = Message.objects.all()
    chat_count = Thread.objects.all()
    assert inbox_count.count() == 2
    assert chat_count.count() == 1


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_send_msg_to_non_existing_user(
    generate_access_token1, websocket_send_dm_message
):
    """
    test sending data to non-existing user
    """
    token, user = generate_access_token1
    message = "Hello non-existing user"
    msg_response = await websocket_send_dm_message(
        token=token, message=message, to="non-existing-user"
    )
    assert msg_response == {
        "error": "user with username 'non-existing-user' does not exist"
    }


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_message_threads(generate_new_token, websocket_send_dm_message):
    """
    test chat threads when sending message between various users
    """
    token1, user1 = generate_new_token(username="user1", password="user1234")
    token2, user2 = generate_new_token(username="user2", password="user2345")
    token3, user3 = generate_new_token(username="user3", password="user3456")
    msg1, msg2, msg3 = "hello user2", "I'm good user1", "hello user1"
    msg_response1 = await websocket_send_dm_message(
        token=token1, message=msg1, to=user2.username
    )
    msg_response2 = await websocket_send_dm_message(
        token=token2, message=msg2, to=user1.username
    )
    chat_thread = Thread.objects.all()
    assert msg_response1["message"]["sender"]["username"] == user1.username
    assert msg_response2["message"]["sender"]["username"] == user2.username
    assert chat_thread.count() == 1
    await websocket_send_dm_message(
        token=token3, message=msg3, to=user1.username
    )
    assert chat_thread.count() == 2
