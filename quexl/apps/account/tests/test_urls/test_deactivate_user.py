from django.urls import reverse


def test_deactivate_user_profile(client, generate_access_token_deactivate):
    """
    test deactivating user profile
    """
    token, user = generate_access_token_deactivate
    id = user.id
    url = reverse("authentication:deactivate_user", args=[id])
    response = client.get(url, HTTP_AUTHORIZATION="Bearer " + token)
    assert response.status_code == 200
    assert response.data["message"] == "Account deactivated successfully."
