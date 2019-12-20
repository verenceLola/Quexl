from django.urls import reverse


def test_get_user_info(client, generate_access_token1):
    """
    test get user info
    """
    token, user = generate_access_token1
    user_url = reverse("authentication:user", args=[user.id])
    response = client.get(user_url, HTTP_AUTHORIZATION="Bearer " + token)
    assert response.data["message"] == "User details fetched successfully"
    assert response.data["details"]["id"] == user.id
    assert response.data["details"]["username"] == user.username
    assert response.status_code == 200


def test_get_user_with_invalid_id(client, generate_access_token1):
    """
    test get user info with invalid id
    """
    token, _ = generate_access_token1
    user_url = reverse(
        "authentication:user", args=[456]
    )  # non existing user id
    response = client.get(user_url, HTTP_AUTHORIZATION="Bearer " + token)
    assert response.data["error"] == "That user id %d does not exist." % 456
    assert response.data["message"] == "Failed to fetch user details"
    assert response.status_code == 404


def test_edit_user_info(client, generate_access_token1, django_user_model):
    """
    test edit user info
    """
    token, user = generate_access_token1
    user_url = reverse("authentication:user", args=[user.id])
    new_details = {"email": "new@email.com"}
    response = client.put(
        user_url,
        new_details,
        HTTP_AUTHORIZATION="Bearer " + token,
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.data["message"] == "User details successfully updated"
    updated_user = django_user_model.objects.get(pk=user.id)
    assert updated_user.email != user.email


def test_getting_current_user_info_without_auth(client):
    """
    test getting current user info with authentication
    """
    me_url = reverse("authentication:me")
    response = client.get(me_url)
    assert response.status_code == 401
    assert (
        "Authentication credentials were not provided.".encode()
        in response.content
    )


def test_getting_current_user_info_with_auth(client, generate_access_token1):
    """
    test getting current user info with credentials/ auth
    """
    token, user = generate_access_token1
    me_url = reverse("authentication:me")
    response = client.get(me_url, HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 200
    assert user.id.encode() in response.content
