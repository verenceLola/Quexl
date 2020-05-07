import pytest

from quexl.apps.account.models import User
from quexl.apps.profiles.models import Address

from .fixtures import signup as fixtures


@pytest.mark.django_db
def test_create_new_user():
    """
    test creating a new db user
    """
    userdata = {
        "username": "user1",
        "email": "user1@email.com",
        "password": None,
    }
    user = User.objects.create_user(**userdata)
    users = User.objects.all()
    assert users.count() == 1
    assert user.is_active  # confirm new user is active


def test_object_string_representation(create_db_user):
    """
    test printing user object prints username
    """
    user = create_db_user
    assert str(user) == user.username


def test_get_user_with_correct_email(create_db_user):
    """
    test getting user with email
    """
    user = create_db_user
    assert User.get_user("user1@quexl.com") == user


def test_get_user_with_wrong_email(create_db_user):
    """
    test getting user with wrong email
    """
    # get non-existing user email
    assert not User.get_user("wrong@email.com")


def test_get_user_by_wrong_id(create_db_user):
    """
    test getting user by wrong id
    """
    assert not User.get_user_by_id("wrong_id")


@pytest.mark.parametrize(
    "user_details, expected_output",
    [
        (
            fixtures.user_details_without_username,
            "Users must have a username.",
        ),  # missing username
        (
            fixtures.user_details_without_email,
            "Users must have an email address.",
        ),  # missing email
    ],
)
def test_create_user(user_details, expected_output):
    """
    test creating new user
    """
    with pytest.raises(TypeError, match=expected_output):
        User.objects.create_user(**user_details)


def test_create_user_without_password(db):
    """
    test creating user without password
    """
    user_details = {"username": "user2", "email": "email2@quexl.com"}
    user = User.objects.create_user(**user_details)
    assert user.password == ""


def test_create_super_user(db):
    super_user_details = {
        "username": "superuser1",
        "password": "pass123",
        "email": "super@email.com",
    }
    super_user = User.objects.create_superuser(**super_user_details)
    assert super_user.is_superuser
    # test create super user without password
    super_user_details["password"] = None

    with pytest.raises(TypeError, match="Superusers must have a password."):
        User.objects.create_superuser(**super_user_details)


def test_address(create_db_user):
    """
    test address creation
    """
    profile = create_db_user.profile
    address_details = {
        "street_address_1": "Site and Service",
        "city": "Nairobi",
        "city_area": "Kasarani",
        "postal_code": "001001",
        "country": "KE",
        "country_area": "Western",
        "phone": "+254713077520",
    }
    address = Address.objects.create(profile=profile, **address_details)
    assert address.address == address_details.get("city")
