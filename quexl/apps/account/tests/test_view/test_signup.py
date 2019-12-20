import pytest
from django.urls import reverse

import quexl.apps.account.tests.fixtures.signup as fixtures


@pytest.mark.parametrize(
    "user_details, expected_response",
    [
        (
            fixtures.correct_user_details,
            fixtures.correct_user_details_response,
        ),
        (
            fixtures.details_without_email,
            fixtures.user_details_without_email_response,
        ),
        (
            fixtures.details_without_username,
            fixtures.user_details_without_username_response,
        ),
        (
            fixtures.invalid_password_user_data,
            fixtures.invalid_password_response,
        ),
        (
            fixtures.long_password_user_data,
            fixtures.long_password_user_data_response,
        ),
    ],
)
@pytest.mark.django_db
def test_register_new_user(client, user_details, expected_response):
    """
    test regestering new user
    """
    signup_url = reverse("authentication:user_signup")
    response = client.post(signup_url, user_details)
    assert response.data == expected_response


def test_signup_user_GET(client):
    """
    test Get method on signup-user endpoint
    """
    signup_url = reverse("authentication:user_signup")
    response = client.get(signup_url)
    assert (
        b"Only POST requests are allowed to this endpoint." in response.content
    )
