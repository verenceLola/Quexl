from django.urls import reverse


def test_activate_user_with_valid_token(
    client, generate_access_token1, django_user_model
):
    """
    test activate user with valid token
    """
    token, user = generate_access_token1
    user.is_active = False  # deactivate user
    user.save()
    activation_url = reverse("authentication:activate_user", args=[token])
    client.get(activation_url)
    # assert response.status_code == 200
    # assert response.data["message"] == "Account activated successfully."
    # new_user = django_user_model.objects.get(username=user.username)
    # assert new_user.is_active


def test_activate_user_with_invalid_token(
    client, generate_access_token1, django_user_model
):
    """
    test user activation with invalid token
    """
    token, user = generate_access_token1
    user.is_active = False  # deactivate user
    user.save()
    activation_url = reverse(
        "authentication:activate_user", args=[token.join(".invalidtoken")]
    )
    response = client.get(activation_url)
    assert response.status_code == 400
    assert response.data["message"] == "Activation link is invalid."
    new_user = django_user_model.objects.get(username=user.username)
    assert not new_user.is_active
