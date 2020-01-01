import pytest
from freezegun import freeze_time

from .fixtures import GroupMessageFixtures

fixtures = GroupMessageFixtures()


@pytest.mark.asyncio
@freeze_time("2019-10-01")
@pytest.mark.django_db(transaction=True)
async def test_send_message_to_group_members(
    generate_access_token1, websocket_send_message, create_user_group
):
    """
    test sending message to group members
    """
    token, user = generate_access_token1
    members = ["user3", "user4"]
    group_name = create_user_group(group_name="group-one", members=members)
    response = await websocket_send_message(
        token=token,
        endpoint="/chat/group/",
        group=group_name,
        message="Hello everyone",
    )
    assert response["message"]["text"] == "Hello everyone"
    assert response["message"]["sender"]["username"] == user.username
    assert response["message"]["sent_at"] == "2019-10-01T00:00:00Z"


@pytest.mark.asyncio
async def test_send_message_to_non_existing_group(
    generate_access_token1, websocket_send_message
):
    """
    test sending group message to non-existing group name
    """
    token, _ = generate_access_token1
    response = await websocket_send_message(
        token=token,
        endpoint="/chat/group/",
        group="non-existing-group",
        message="Hello no one",
    )
    assert response == fixtures.non_exisiting_group_response


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_send_group_message_when_not_group_member(
    generate_access_token2, create_user_group, websocket_send_message
):
    """
    test sending group message when not a group member
    """
    token, user = generate_access_token2
    members = ["user3", "user4"]
    group_name = create_user_group(group_name="new-group", members=members)
    response = await websocket_send_message(
        token=token,
        endpoint="/chat/group/",
        group=group_name,
        message="Hello everyone",
    )
    assert response == fixtures.non_member_response
