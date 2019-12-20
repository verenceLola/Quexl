from django.urls import reverse
from rolepermissions.roles import get_user_roles

from quexl.apps.roles.roles import DeveloperRole


def test_assign_user_roles_with_inadequest_permisions(
    client, generate_access_token1, create_db_user2
):
    """
    test assign user roles without adequent permissions
    """
    access_token, user = generate_access_token1
    user = create_db_user2
    roles_url = reverse("roles:user roles", args=[user.id])
    request = client.post(
        roles_url,
        {"role": "regular_user"},
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 403
    assert request.data["error"] == "You don't have permission to assign roles"
    assert request.data["message"] == "Assign user role failed"


def test_assign_role_to_non_existing_user(
    client, generate_superuser_access_token
):
    """
    test assign role to non-exting user id
    """
    access_token = generate_superuser_access_token
    roles_url = reverse("roles:user roles", args=["non-existing-id"])
    request = client.post(
        roles_url,
        {"role": "regular_user"},
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 404
    assert (
        request.data["error"] == "User with id non-existing-id does not exist"
    )
    assert request.data["message"] == "Assign user role failed"


def test_assign_user_role_as_superuser(
    client, generate_superuser_access_token, create_db_user2
):
    """
    test assign role to user as superuser
    """
    access_token = generate_superuser_access_token
    user = create_db_user2
    roles_url = reverse("roles:user roles", args=[user.id])
    request = client.post(
        roles_url,
        {"role": "developer"},
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert (
        request.data["message"] == "User assigned developer role successfully"
    )
    assert DeveloperRole in get_user_roles(user)


def test_assign_role_without_role_data(
    client, generate_superuser_access_token, create_db_user
):
    """
    test assign role wthout user role data
    """
    access_token = generate_superuser_access_token
    user = create_db_user
    roles_url = reverse("roles:user roles", args=[user.id])
    request = client.post(
        roles_url, HTTP_AUTHORIZATION="Bearer " + access_token
    )
    assert request.data["error"] == "Missing role field"
    assert request.data["message"] == "Assign user role failed"
    assert request.status_code == 400


def test_assign_non_existing_user_role(
    client, generate_superuser_access_token, create_db_user
):
    """
    test assigning non existing user role
    """
    access_token = generate_superuser_access_token
    user = create_db_user
    roles_url = reverse("roles:user roles", args=[user.id])
    request = client.post(
        roles_url,
        {"role": "non-existing-role"},
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 404
    assert (
        request.data["error"] == "Role named non-existing-role does not exist"
    )
    assert request.data["message"] == "Assign user role failed"
