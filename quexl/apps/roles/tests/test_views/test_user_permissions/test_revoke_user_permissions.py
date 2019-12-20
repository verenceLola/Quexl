"""
test user roles and permissions views
"""
from django.urls import reverse
from rolepermissions.checkers import has_permission
from rolepermissions.roles import assign_role


def test_delete_permission_with_missing_permission_field(
    client, generate_superuser_access_token, create_db_user
):
    """
    test revoke user permision without permission field
    """
    user = create_db_user
    perm_url = reverse("roles:user permissions", args=[user.id])
    access_token = generate_superuser_access_token
    request = client.delete(
        perm_url,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 400
    assert request.data["error"] == "Missing permission field"
    assert request.data["message"] == "Revoke user permission failed"


def test_revoke_permission_with_insuffient_permissions(
    client, generate_access_token1, create_db_user2
):
    """
    test revoke permission without adequate permissions
    """
    user = create_db_user2
    perm_url = reverse("roles:user permissions", args=[user.id])
    access_token, _ = generate_access_token1
    request = client.delete(
        perm_url,
        {"permission": "view_user_roles"},
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 403
    assert (
        request.data["error"]
        == "You do not have permission to revoke user permissions"
    )
    assert request.data["message"] == "Revoke user permission failed"


def test_revoke_permission_non_existing_user(
    client, generate_superuser_access_token
):
    """
    test revoke user permissionsfor non existing user
    """
    perm_url = reverse("roles:user permissions", args=["non-existing-user-id"])
    access_token = generate_superuser_access_token
    request = client.delete(
        perm_url,
        {"permission": "view_user_roles"},
        content_type="application/json",
        HTTP_AUTHORIZATION="bearer " + access_token,
    )
    assert request.status_code == 404
    assert (
        request.data["error"]
        == "User with id non-existing-user-id does not exist"
    )
    assert request.data["message"] == "Revoke user permission failed"


def test_revoke_wrong_permissiong_for_user_role(
    client, generate_superuser_access_token, create_db_user
):
    """
    test revoke wrong user permssion
    """
    user = create_db_user
    perm_url = reverse("roles:user permissions", args=[user.id])
    access_token = generate_superuser_access_token
    request = client.delete(
        perm_url,
        {"permission": "invalid_role_permission"},
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 400
    assert (
        request.data["error"]
        == "User missing required role(s) for invalid_role_permission permission"
    )
    assert request.data["message"] == "Revoke user permission failed"


def test_revoke_permission_as_superuser(
    client, generate_superuser_access_token, create_db_user
):
    """
    test revoke user permission as superuser
    """
    user = create_db_user
    perm_url = reverse("roles:user permissions", args=[user.id])
    access_token = generate_superuser_access_token
    assign_role(user, "site_admin")
    request = client.delete(
        perm_url,
        {"permission": "assign_user_roles"},
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.data["message"] == "user permission revoked successfully"
    assert request.status_code == 200
    assert request.data["data"]["permission_revoked"] == "assign_user_roles"
    assert not has_permission(user, "assign_user_roles")
