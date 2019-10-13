"""
configure common methods for testing
"""
import pytest
from quexl.apps.authentication.backends import JWTAuthentication


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
    return superuser
