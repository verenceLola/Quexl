"""
configure common methods for testing
"""
import pytest
from quexl.apps.account.backends import JWTAuthentication


@pytest.fixture
def create_db_user(django_user_model):
    """
    create a db user
    """
    user_details = {
        "username": "user1",
        "password": "pass123",
        "email": "user1@quexl.com",
    }
    user1 = django_user_model.objects.create_user(**user_details)
    user1.is_active = True  # activate user account
    user1.save()
    return user1


@pytest.fixture
def generate_access_token1(create_db_user):
    """
    """
    user1 = create_db_user
    user_details = {"username": user1.username, "email": user1.email}
    jwt = JWTAuthentication()
    encoded_token = jwt.generate_token(user_details)
    return encoded_token, user1


@pytest.fixture
def create_superuser(django_user_model):
    superuser_details = {
        "username": "superuser1",
        "password": "passSuper3",
        "email": "super@quexl.com",
    }
    superuser = django_user_model.objects.create_superuser(**superuser_details)
    superuser.is_active = True
    superuser.save()
    return superuser


@pytest.fixture()
def generate_superuser_access_token(create_superuser):
    """
    generate superuser token
    """
    superuser = create_superuser
    details = {"username": superuser.username, "email": superuser.email}
    jwt = JWTAuthentication()
    encoded_token = jwt.generate_token(details)
    return encoded_token


@pytest.fixture
def create_db_user2(django_user_model):
    """
    create a db user
    """
    user_details = {
        "username": "user2",
        "password": "pass123",
        "email": "user2@quexl.com",
    }
    user2 = django_user_model.objects.create_user(**user_details)
    user2.is_active = True  # activate user account
    user2.save()
    return user2
