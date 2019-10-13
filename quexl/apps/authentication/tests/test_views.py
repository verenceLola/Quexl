import pytest
from django.urls import reverse
from .fixtures import (
    details_without_email,
    user_details_without_email_response,
    details_without_username,
    user_details_without_username_response,
    correct_user_details,
    correct_user_details_response,
    invalid_password_response,
    invalid_password_user_data,
    long_password_user_data,
    long_password_user_data_response,
    signup_user_GET_response,
    login_failed_response,
    invalid_login_password,
    invalid_login_email,
    correct_login_details,
    blank_email_login_response,
    blank_email_login,
    missing_email_login,
    blank_password_login_response,
    blank_password_login,
    correct_login_response,
    valid_reset_token,
    reset_password_response,
    reset_password_invalid_token_response,
    missing_password_login,
    missing_email_login_response,
    missing_password_login_response,
)


@pytest.mark.parametrize(
    "user_details, expected_response",
    [
        (correct_user_details, correct_user_details_response),
        (details_without_email, user_details_without_email_response),
        (details_without_username, user_details_without_username_response),
        (invalid_password_user_data, invalid_password_response),
        (long_password_user_data, long_password_user_data_response),
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
    assert response.data == signup_user_GET_response["response"]


@pytest.mark.parametrize(
    "login_details, expected_response",
    [
        (invalid_login_email, login_failed_response),
        (invalid_login_password, login_failed_response),
        (blank_email_login, blank_email_login_response),
        (blank_password_login, blank_password_login_response),
        (correct_login_details, correct_login_response),
        (missing_email_login, missing_email_login_response),
        (missing_password_login, missing_password_login_response),
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
        assert response.data == expected_response


@pytest.mark.parametrize(
    "reset_token, expected_response",
    [
        (valid_reset_token, reset_password_response),
        ("ivalidtoke", reset_password_invalid_token_response),
    ],
)
def test_reset_password(
    client, create_db_user, reset_token, expected_response
):
    """
    test reset user password
    """
    # user = create_db_user
    reset_url = reverse("authentication:reset_password", args=[reset_token])
    response = client.put(reset_url)
    assert response.data == expected_response
