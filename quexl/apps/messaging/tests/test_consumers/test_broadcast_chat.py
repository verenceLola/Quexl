import pytest
from freezegun import freeze_time

from quexl.apps.messaging.models import Thread


@pytest.mark.asyncio
@freeze_time("2019-10-01")
@pytest.mark.django_db(transaction=True)
async def test_send_broadcast_message(
    generate_new_token, websocket_send_message
):
    """
    test sending broadcast message to various users
    """
    token1, user1 = generate_new_token(username="user1")
    token2, user2 = generate_new_token(username="user2")
    token3, user3 = generate_new_token(username="user3")
    token4, user4 = generate_new_token(username="user4")
    to_users = [
        {"username": user2.username},
        {"username": user3.username},
        {"username": user4.username},
    ]
    response1 = await websocket_send_message(
        token=token1,
        message="Hello guys",
        endpoint="/chat/broadcast/",
        to=to_users,
    )
    threads = Thread.objects.all()
    current_thread = Thread.objects.get(pk=response1["message"]["chatId"])
    assert current_thread.type == "dm"
    assert threads.count() == 3
    assert response1["message"]["sent_at"] == "2019-10-01T00:00:00Z"
    assert response1["message"]["sender"]["username"] == user1.username


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_send_broadcast_to_non_existing_users(
    generate_new_token, websocket_send_message
):
    """
    test broadcasting message to existing and non-existing users
    """
    token1, user1 = generate_new_token(username="user1")
    token2, user2 = generate_new_token(username="user2")
    to_users = [{"username": "username"}, {"username": user2.username}]
    response = await websocket_send_message(
        token=token1,
        message="Hello my people",
        endpoint="/chat/broadcast/",
        to=to_users,
    )
    threads = Thread.objects.all()
    assert threads.count() == 1
    current_thread = Thread.objects.get(pk=response["message"]["chatId"])
    assert current_thread.type == "dm"
    assert (
        "Failed to send message to the following users."
        in response["errors"]["message"]
    )
    assert len(response["errors"]["users"]) == 1
    assert response["errors"]["users"][0]["username"] == "username"
