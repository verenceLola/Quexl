import pytest
from django.urls import reverse

import quexl.apps.account.tests.fixtures.password as fixtures


@pytest.mark.parametrize(
    "reset_token, expected_response",
    [
        (fixtures.valid_reset_token, fixtures.reset_password_response),
        ("invalidtoken", fixtures.reset_password_invalid_token_response),
    ],
)
def test_reset_password(
    client, create_db_user, reset_token, expected_response
):
    """
    test reset user password
    """
    reset_url = reverse("authentication:reset_password", args=[reset_token])
    response = client.put(reset_url)
    assert response.data == expected_response


def test_forgot_password(client, create_db_user):
    """
    test forgot user password view
    """
    user = create_db_user
    forgot_password_url = reverse("authentication:forgot_password")
    response = client.post(forgot_password_url, {"email": user.email})
    assert response.data == {
        "message": "An email has been sent to your inbox with a password reset link."
    }
    assert response.status_code == 200


@pytest.mark.django_db
def test_forgot_password_with_invalid_email(client):
    """
    test forgot user password with non-existing email
    """
    forgot_password_url = reverse("authentication:forgot_password")
    response = client.post(forgot_password_url, {"email": "wrong@email.com"})
    assert response.data["error"] == "Missing or non-existing email."
    assert response.data["message"] == "Password Reset Request failed"
    assert response.status_code == 404
