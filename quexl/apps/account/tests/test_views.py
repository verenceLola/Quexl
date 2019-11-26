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
    invalid_login_email_response,
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
    assert (
        b"Only POST requests are allowed to this endpoint." in response.content
    )


@pytest.mark.parametrize(
    "login_details, expected_response",
    [
        (invalid_login_email, invalid_login_email_response),
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
        assert expected_response["message"].encode() in response.content
        assert expected_response["error"].encode() in response.content


@pytest.mark.parametrize(
    "reset_token, expected_response",
    [
        (valid_reset_token, reset_password_response),
        ("invalidtoken", reset_password_invalid_token_response),
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
    print(response.data)
    assert response.status_code == 200
    assert response.data["message"] == "User details successfully updated"
    updated_user = django_user_model.objects.get(pk=user.id)
    assert updated_user.email != user.email
