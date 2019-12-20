from django.urls import reverse
from rolepermissions.roles import get_user_roles

from quexl.apps.roles.roles import RegularUserRole


def test_delete_role_for_non_existing_user_id(
    client, generate_superuser_access_token
):
    """
    test delete role for non existing user id
    """
    access_token = generate_superuser_access_token
    roles_url = reverse("roles:user roles", args=["non-existing-user-id"])
    request = client.delete(
        roles_url,
        {"role": "developer"},
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 404
    assert (
        request.data["error"]
        == "User with id non-existing-user-id does not exist"
    )
    assert request.data["message"] == "Remove user role failed"


def test_delete_non_existing_role(
    client, generate_superuser_access_token, create_db_user
):
    """
    test delete non existing user role
    """
    access_token = generate_superuser_access_token
    user = create_db_user
    roles_url = reverse("roles:user roles", args=[user.id])
    request = client.delete(
        roles_url,
        {"role": "non-existing-role"},
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert (
        request.data["error"] == "Role named non-existing-role does not exist"
    )
    assert request.data["message"] == "Remove user role failed"


def test_delete_user_role_with_inadequete_permission(
    client, generate_access_token1, create_db_user2
):
    """
    test remove user role with inadequate permissions
    """
    access_token, _ = generate_access_token1
    user = create_db_user2
    roles_url = reverse("roles:user roles", args=[user.id])
    request = client.delete(
        roles_url,
        {"role": "developer"},
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 403
    assert (
        request.data["error"]
        == "You don't have permission to remove user roles"
    )
    assert request.data["message"] == "Remove user role failed"


def test_remove_user_role(
    client, generate_superuser_access_token, create_db_user
):
    """
    test remove user role
    """
    user = create_db_user
    access_token = generate_superuser_access_token
    roles_url = reverse("roles:user roles", args=[user.id])
    request = client.delete(
        roles_url,
        {"role": "regular_user"},
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 200
    assert (
        request.data["message"]
        == "User role regular_user removed successfully"
    )
    assert RegularUserRole not in get_user_roles(user)


def test_remove_role_without_role_field(
    client, generate_superuser_access_token, create_db_user
):
    """
    test remove user role without role field
    """
    access_token = generate_superuser_access_token
    user = create_db_user
    role_url = reverse("roles:user roles", args=[user.id])
    request = client.delete(
        role_url,
        content_type="appplication/json",
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 400
    assert request.data["message"] == "Remove user role failed"
    assert request.data["error"] == "Missing role field"
