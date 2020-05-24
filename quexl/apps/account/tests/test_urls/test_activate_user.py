from django.urls import reverse


def test_deactivate_user_profile(
    client, generate_access_token_deactivate, generate_superuser_access_token
):
    """
    test activating user profile
    """
    _, user = generate_access_token_deactivate
    token = generate_superuser_access_token
    id = user.id
    reverse("authentication:deactivate_user", args=[id])
    url = reverse("authentication:activate", args=[id])
    response = client.get(url, HTTP_AUTHORIZATION="Bearer " + token)
    assert response.status_code == 200
    assert response.data["message"] == "Account activated successfully."
