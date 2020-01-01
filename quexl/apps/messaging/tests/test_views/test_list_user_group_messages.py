import json

import pytest
from django.urls import reverse

from quexl.apps.messaging.models import Thread

URL = reverse("messaging:user-group-messages")


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_list_user_group_messages(
    client, create_user_group, websocket_send_message, generate_access_token1
):
    """
    test listing group messages for a given user
    """
    token, user = generate_access_token1
    members = ["user2", "user3"]
    group_name = create_user_group(group_name="group-one", members=members)
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert len(response.data) == 0
    ws_response = await websocket_send_message(
        token=token,
        endpoint="/chat/group/",
        group=group_name,
        message="Hello guys",
    )
    assert ws_response["message"]["sender"]["username"] == user.username
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp_content = json.loads(response.content.decode())
    assert resp_content["status"] == "success"
    assert len(resp_content["data"][0]["messages"]) == 1
    ws_response = await websocket_send_message(
        token=token,
        endpoint="/chat/group/",
        group=group_name,
        message="Hello guys",
    )
    assert response.status_code == 200
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert len(response.data[0]["messages"]) == 2
    assert (
        len(
            list(
                filter(
                    lambda x: x["sender"]["username"] == user.username,
                    response.data[0]["messages"],
                )
            )
        )
        == 2
    )
    threads = Thread.objects.all()
    assert len(list(filter(lambda x: x.type == "group", threads))) == 1
