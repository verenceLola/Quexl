import json

from django.urls import reverse

from ..fixtures import ChatGroup as ChatGroupClass

URL = reverse("messaging:user-groups")
ChatGroup = ChatGroupClass()


def test_list_user_group(client, generate_access_token1, create_user_group):
    """
    test listing user groups
    """
    token, user = generate_access_token1
    members = ["user2", "user3", "user4"]
    create_user_group(group_name="group-one", members=members)
    response = client.get(URL, HTTP_AUTHORIZATION=f"Bearer {token}")
    resp = json.loads(response.content.decode())
    assert response.status_code == 200
    assert resp["status"] == "success"
    assert resp["data"][0]["group_name"] == "group-one"
    assert not resp["data"][0]["last_message"]
    assert (
        len(
            list(
                filter(
                    lambda x: x["username"] == user.username,
                    resp["data"][0]["members"],
                )
            )
        )
        == 1
    )
