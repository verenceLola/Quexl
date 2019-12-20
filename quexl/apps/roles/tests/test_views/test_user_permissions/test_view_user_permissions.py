from django.urls import reverse
from rolepermissions.roles import assign_role


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
        request.data["error"] == "User does not have any permissions assigned"
    )
    assert request.data["message"] == "View user permissions failed"
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
    assert request.data["message"] == "View user permissions failed"
    assert request.data["error"] == "You don't have any permissions"


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
        request.data["error"]
        == "User with id non-existing-user-id does not exist"
    )
    assert request.data["message"] == "View user permissions failed"
