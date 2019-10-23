"""
test authentication backends
"""
from quexl.apps.account.backends import JWTAuthentication
import pytest
import freezegun
import datetime
from rest_framework.exceptions import AuthenticationFailed


@pytest.fixture
def setup_jwt():
    return JWTAuthentication()


@freezegun.freeze_time("2019-08-10")
def generate_expired_token():
    user_data = {"username": "username1", "email": "email@quexl.com"}
    return JWTAuthentication().generate_token(user_data)


@freezegun.freeze_time("2019-10-13 12:00:00")
def test_encode_decode_token(setup_jwt):
    """
    test generate token
    """
    jwt = setup_jwt
    user_data = {"username": "username2", "email": "email@quexl.com"}
    encoded_token = jwt.generate_token(user_data)
    decoded_token = jwt.decode_jwt(encoded_token)
    assert decoded_token["userdata"] == user_data
    assert (
        decoded_token["iat"]
        == datetime.datetime(2019, 10, 13, 12, 00, 00).timestamp()
    )
    assert (
        decoded_token["exp"]
        == (
            datetime.datetime(2019, 10, 13, 12, 00, 00)
            + datetime.timedelta(days=7)
        ).timestamp()
    )


@freezegun.freeze_time("2019-10-13 12:00:00")
def test_generate_reset_token(setup_jwt, settings):
    """
    test generate reset token
    """
    jwt = setup_jwt
    email = "email@quexl.com"
    reset_token = jwt.generate_reset_token(email)
    decoded_token = jwt.decode_jwt(reset_token)
    assert decoded_token["email"] == email
    assert (
        decoded_token["iat"]
        == datetime.datetime(2019, 10, 13, 12, 00, 00).timestamp()
    )
    assert decoded_token["jti"] == settings.SECRET_KEY
    assert (
        decoded_token["exp"]
        == (
            datetime.datetime(2019, 10, 13, 12, 00, 00)
            + datetime.timedelta(minutes=720)
        ).timestamp()
    )


def test_authenticate_credentials_with_valid_token(
    generate_access_token1, setup_jwt
):
    """
    test authenticate user credentials with valid token
    """
    token, user1 = generate_access_token1
    jwt = setup_jwt
    user, user_details = jwt.authenticate_credentials(token)
    assert user == user1
    assert user_details["userdata"]["username"] == user1.username
    assert user_details["userdata"]["email"] == user1.email


@pytest.mark.parametrize(
    "token, expected_message",
    [
        ("jd*djd^#bdhdyd", "Invalid token"),
        (generate_expired_token(), "Token has expired"),
    ],
)
def test_authenticate_credentials_with_invalid_token(
    setup_jwt, token, expected_message
):
    """
    test authenticate user credentials with invalid token
    """
    jwt = setup_jwt
    with pytest.raises(AuthenticationFailed, match=expected_message):
        jwt.authenticate_credentials(token)


def test_authenticate_credentials_for_inactive_user(
    setup_jwt, create_db_user, generate_access_token1
):
    """
    test authenticate credentials for inactive user
    """
    token, _ = generate_access_token1
    user = create_db_user
    user.is_active = False  # deactivate user account
    user.save()
    jwt = setup_jwt
    with pytest.raises(AuthenticationFailed, match="User inactive or deleted"):
        jwt.authenticate_credentials(token)
