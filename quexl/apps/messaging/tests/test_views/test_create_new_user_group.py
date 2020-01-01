from django.urls import reverse

URL = reverse("messaging:user-groups")


def test_create_group_without_members_field(client, generate_access_token1):
    """
    test creating new group without supplying group members
    """
    token, _ = generate_access_token1
    response = client.post(
        URL,
        {"group_name": "valid-group-name"},
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )
    assert response.status_code == 422
