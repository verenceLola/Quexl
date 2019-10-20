"""
test user roles and permissions views
"""
from django.urls import reverse
from rolepermissions.roles import get_user_roles, assign_role
from rolepermissions.checkers import has_permission
from quexl.apps.roles.roles import Developer, RegularUser


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
    assert (
        request.data["message"]
        == "User with id non-existing-id does not exist"
    )
    assert request.status_code == 404


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
    assert (
        request.data["message"] == "You don't have permission to assign roles"
    )


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
        request.data["message"]
        == "User with id non-existing-id does not exist"
    )


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
    assert Developer in get_user_roles(user)


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
    assert request.data["message"] == "Missing role field"
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
        request.data["message"]
        == "Role named non-existing-role does not exist"
    )


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
        request.data["message"]
        == "User with id non-existing-user-id does not exist"
    )


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
        request.data["message"]
        == "Role named non-existing-role does not exist"
    )


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
        request.data["message"]
        == "You don't have permission to remove user roles"
    )


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
    assert RegularUser not in get_user_roles(user)


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
    assert request.data["message"] == "Missing role field"


def test_get_user_permissions_as_superuser(
    client, create_db_user, generate_superuser_access_token
):
    """
    test get user permissions as super user
    """
    access_token = generate_superuser_access_token
    user = create_db_user
    perm_url = reverse("roles:user permissions", args=[user.id])
    request = client.get(perm_url, HTTP_AUTHORIZATION="Bearer " + access_token)
    assert request.status_code == 200
    assert (
        request.data["message"]
        == "User does not have any permissions assigned"
    )
    assign_role(user, "site_admin")
    request = client.get(perm_url, HTTP_AUTHORIZATION="Bearer " + access_token)
    assert request.data["message"] == "User has the following permmissions"


def test_get_user_permissions_with_inadequate_permssions(
    client, generate_access_token1, create_db_user2
):
    """
    test get user token with insuffient permissions shows own permissions
    """
    access_token, db_user = generate_access_token1
    user = create_db_user2
    perm_url = reverse("roles:user permissions", args=[user.id])
    request = client.get(perm_url, HTTP_AUTHORIZATION="Bearer " + access_token)
    assert request.status_code == 200
    assert request.data["message"] == "You don't have any permissions"


def test_get_permission_for_non_existing_user(
    client, generate_superuser_access_token
):
    """
    test get user permissions for non existing user id
    """
    access_token = generate_superuser_access_token
    perm_url = reverse("roles:user permissions", args=["non-existing-user-id"])
    request = client.get(perm_url, HTTP_AUTHORIZATION="Bearer " + access_token)
    assert request.status_code == 404
    assert (
        request.data["message"]
        == "User with id non-existing-user-id does not exist"
    )


def test_assign_permission_with_missing_permission_field(
    client, generate_superuser_access_token, create_db_user
):
    """
    test assign permission with missing permission field
    """
    user = create_db_user
    perm_url = reverse("roles:user permissions", args=[user.id])
    access_token = generate_superuser_access_token
    request = client.post(
        perm_url, HTTP_AUTHORIZATION="Bearer " + access_token
    )
    assert request.status_code == 400
    assert request.data["message"] == "Missing permission field"


def test_assign_permission_as_superuser(
    client, generate_superuser_access_token, create_db_user
):
    """
    test assign permission as superuser
    """
    user = create_db_user
    perm_url = reverse("roles:user permissions", args=[user.id])
    access_token = generate_superuser_access_token
    assign_role(user, "developer")  # assign requred role for permission
    request = client.post(
        perm_url,
        {"permission": "view_user_roles"},
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 201
    assert (
        request.data["message"]
        == "User assigned view_user_roles permission successfully"
    )
    assert has_permission(user, "view_user_roles")


def test_assign_permission_with_inadequate_permissions(
    client, generate_access_token1, create_db_user2
):
    """
    test assign permission without necessary permissions
    """
    user = create_db_user2
    perm_url = reverse("roles:user permissions", args=[user.id])
    access_token, _ = generate_access_token1
    request = client.post(
        perm_url,
        {"permission": "view_user_roles"},
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 403
    assert (
        request.data["message"]
        == "You do not have permission to assign user permissions"
    )


def test_assign_permission_to_non_existing_user(
    client, generate_superuser_access_token
):
    """
    test assign non exitsing user permission
    """
    perm_url = reverse("roles:user permissions", args=["non-existing-user-id"])
    access_token = generate_superuser_access_token
    request = client.post(
        perm_url,
        {"permission": "view_user_roles"},
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 404
    assert (
        request.data["message"]
        == "User with id non-existing-user-id does not exist"
    )


def test_assign_wrong_permission_as_superuser(
    client, generate_superuser_access_token, create_db_user
):
    """
    test assign wrong permission to user with invalid role
    """
    user = create_db_user
    perm_url = reverse("roles:user permissions", args=[user.id])
    access_token = generate_superuser_access_token
    request = client.post(
        perm_url,
        {"permission": "view_user_roles"},
        HTTP_AUTHORIZATION="Bearer " + access_token,
    )
    assert request.status_code == 400
    assert (
        request.data["message"]
        == "User missing required role(s) for view_user_roles permission"
    )


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
    assert request.data["message"] == "Missing permission field"


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
        request.data["message"]
        == "You do not have permission to revoke user permissions"
    )


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
        request.data["message"]
        == "User with id non-existing-user-id does not exist"
    )


def test_revoke_wrong_permissiong_for_user_role(
    client, generate_superuser_access_token, create_db_user
):
    """
    test tevoke wrong user permssion
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
        request.data["message"]
        == "User missing required role(s) for invalid_role_permission permission"
    )


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
