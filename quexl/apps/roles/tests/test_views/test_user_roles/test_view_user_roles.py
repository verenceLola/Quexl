from django.urls import reverse


def test_user_can_view_their_roles(generate_access_token1, client):
    """
    test user can view roles
    """
    access_token, user1 = generate_access_token1
    roles_url = reverse("roles:user roles", args=[user1.id])
    request = client.get(
        roles_url, HTTP_AUTHORIZATION="Bearer " + access_token
    )
    assert request.data["message"] == "You have the following roles"
    assert request.data["data"][0]["name"] == "regular_user"


def test_super_user_can_view_all_roles(
    client, generate_superuser_access_token, create_db_user
):
    """
    test super user can view all user's roles
    """
    user = create_db_user
    access_token = generate_superuser_access_token
    roles_url = reverse("roles:user roles", args=[user.id])
    request = client.get(
        roles_url, HTTP_AUTHORIZATION="Bearer " + access_token
    )
    assert request.data["message"] == "User has the following roles"


def test_get_user_roles_for_non_existing_user(
    client, generate_superuser_access_token
):
    """
    test getting userroles for non existing user
    """
    access_token = generate_superuser_access_token
    roles_url = reverse("roles:user roles", args=["non-existing-id"])
    request = client.get(
        roles_url, HTTP_AUTHORIZATION="Bearer " + access_token
    )
    assert request.data["message"] == "View user roles failed"
    assert (
        request.data["error"] == "User with id non-existing-id does not exist"
    )
    assert request.status_code == 404
