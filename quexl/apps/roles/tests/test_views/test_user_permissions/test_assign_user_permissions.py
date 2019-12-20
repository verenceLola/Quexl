from django.urls import reverse
from rolepermissions.checkers import has_permission
from rolepermissions.roles import assign_role


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
    assert request.data["error"] == "Missing permission field"
    assert request.data["message"] == "Assign user permission failed"


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
        request.data["error"]
        == "You do not have permission to assign user permissions"
    )
    assert request.data["message"] == "Assign user permission failed"


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
        request.data["error"]
        == "User with id non-existing-user-id does not exist"
    )
    assert request.data["message"] == "Assign user permission failed"


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
        request.data["error"]
        == "User missing required role(s) for view_user_roles permission"
    )
    assert request.data["message"] == "Assign user permission failed"
