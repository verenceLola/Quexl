import pytest
from django.urls import reverse

from ..fixtures import login as fixtures


@pytest.mark.parametrize(
    "login_details, expected_response",
    [
        (fixtures.invalid_login_email, fixtures.invalid_login_email_response),
        (fixtures.invalid_login_password, fixtures.login_failed_response),
        (fixtures.blank_email_login, fixtures.blank_email_login_response),
        (
            fixtures.blank_password_login,
            fixtures.blank_password_login_response,
        ),
        (fixtures.correct_login_details, fixtures.correct_login_response),
        (fixtures.missing_email_login, fixtures.missing_email_login_response),
        (
            fixtures.missing_password_login,
            fixtures.missing_password_login_response,
        ),
    ],
)
def test_user_login(client, create_db_user, login_details, expected_response):
    """
    test login user
    """
    login_url = reverse("authentication:user_login")
    response = client.post(login_url, login_details)

    if response.status_code == 200:
        assert response.data["message"] == expected_response
    else:
        assert expected_response["message"].encode() in response.content
        assert expected_response["error"].encode() in response.content
