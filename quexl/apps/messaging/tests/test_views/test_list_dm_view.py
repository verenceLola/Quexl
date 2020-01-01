import json

import pytest
from django.urls import reverse


def test_list_empty_dm_messages(client, generate_access_token1):
    """
    test listing dm messages with empty inbox
    """
    token, _ = generate_access_token1
    url = reverse("messaging:user-dm-messages")
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert json.loads(response.content.decode())["status"] == "success"
    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_list_dm_message(
    client,
    generate_access_token1,
    generate_access_token2,
    generate_new_token,
    websocket_send_message,
):
    """
    test list dm messages
    """
    token, user1 = generate_access_token1
    token2, user2 = generate_access_token2
    token3, _ = generate_new_token(username="user3", password="user3456")
    url = reverse("messaging:user-dm-messages")
    await websocket_send_message(
        token=token,
        to=user2.username,
        message="hello user2",
        endpoint="/chat/dm/",
    )
    response = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 200
    msgs = list(
        filter(
            lambda x: list(
                filter(
                    lambda y: y["sender"]["username"] == user1.username,
                    x["messages"],
                )
            ),
            response.data,
        )
    )
    assert len(msgs) == 1
    response2 = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token2}")
    msgs2 = list(
        filter(
            lambda x: list(
                filter(
                    lambda y: y["sender"]["username"] == user1.username,
                    x["messages"],
                )
            ),
            response2.data,
        )
    )
    assert len(msgs2) == 1
    response3 = client.get(url, HTTP_AUTHORIZATION=f"Bearer {token3}")
    assert response3.data == []
