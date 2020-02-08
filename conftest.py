"""
configure common methods for testing
"""
import os
from typing import Callable
from typing import Tuple
from typing import Type

import pytest
from django.core.files import File

from quexl.apps.account.backends import JWTAuthentication
from quexl.apps.account.models import User
from quexl.apps.services.models import Category
from quexl.apps.services.models import DataFormat
from quexl.apps.services.models import Gallery
from quexl.apps.services.models import OutputFile
from quexl.apps.services.models import ParameterOption
from quexl.apps.services.models import ParameterTemplate
from quexl.apps.services.models import Service


@pytest.fixture
def create_db_user(django_user_model: Type[User]) -> User:
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
def generate_access_token1(create_db_user: User) -> Tuple[str, User]:
    """
    """
    user1 = create_db_user
    user_details = {"username": user1.username, "email": user1.email}
    jwt = JWTAuthentication()
    encoded_token = jwt.generate_token(user_details)
    return encoded_token, user1


@pytest.fixture
def generate_access_token2(create_db_user2: User) -> Tuple[str, User]:
    """
    """
    user2 = create_db_user2
    user_details = {"username": user2.username, "email": user2.email}
    jwt = JWTAuthentication()
    encoded_token = jwt.generate_token(user_details)
    return encoded_token, user2


@pytest.fixture
def create_superuser(django_user_model: Type[User]) -> User:
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
def generate_superuser_access_token(create_superuser: User) -> str:
    """
    generate superuser token
    """
    superuser = create_superuser
    details = {"username": superuser.username, "email": superuser.email}
    jwt = JWTAuthentication()
    encoded_token = jwt.generate_token(details)
    return encoded_token


@pytest.fixture
def create_db_user2(django_user_model: Type[User]) -> User:
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


@pytest.fixture()
def generate_new_token(django_user_model: Type[User]) -> Callable:
    """
    generate new jwt tokn for givn user credentials
    """

    def _generate_new_token(**kwargs):
        username = kwargs.get("username")
        details = {
            "username": username,
            "password": kwargs.get("password", "pass1234"),
            "email": f"{username}@quexl.com",
        }
        user = django_user_model.objects.create(**details)
        user.is_active = True  # activate user
        user.save()
        details.pop("password")  # remove password from jwt payload
        jwt = JWTAuthentication()
        token = jwt.generate_token(details)

        return token, user

    return _generate_new_token


"""configure common testing methods"""


@pytest.fixture
def create_category(db) -> Category:
    """create a category instance"""
    category_details = {
        "name": "category_one",
    }
    cat1 = Category.objects.create(**category_details)
    cat1.save()
    return cat1


@pytest.fixture
def create_category2(create_category):
    """create a category 2nd instance"""
    cat = Category()
    cat.name = "sub_category"
    cat.parent_id = create_category.id
    cat.save()
    return cat


@pytest.fixture
def create_category3(db):
    """create a category 3rd instance"""
    cat = Category()
    cat.name = "to_delete"
    cat.save()
    return cat


@pytest.fixture
def create_service(create_db_user):
    """create a service instance"""
    service = Service()
    service.name = "Online file conversion"
    service.api_endpoint = "https://sandbox.zamzar.com/v1/jobs"
    service.delivery_time = "2070-11-01 21:40:53.028781+03"
    service.price.amount = "0"
    service.price.currency = "kes"
    service.seller_id = create_db_user.id
    service.save()
    return service


@pytest.fixture
def create_gallery(create_service):
    """create a gallery instance"""
    if not os.path.exists("./test_images"):
        os.mkdir("./test_images")
    im = open("./test_images/img.jpg", "w")
    image = File(im)
    gallery = Gallery()
    gallery.service = create_service
    gallery.image = image.file.name
    gallery.description = "Image description"
    gallery.save()
    if os.path.exists("./test_images"):
        if os.path.exists("./test_images/img.jpg"):
            os.remove("./test_images/img.jpg")
        os.rmdir("./test_images")
    return gallery


@pytest.fixture
def create_data_format(db):
    """create a dataformat instance"""
    data_format_details = {
        "name": "data format",
    }
    data_format = DataFormat.objects.create(**data_format_details)
    data_format.save()
    return data_format


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def create_jpg_data_format(db):
    """create a jpg dataformat instance"""
    data_format_details = {
        "name": "jpg",
    }
    data_format = DataFormat.objects.create(**data_format_details)
    data_format.save()
    return data_format


@pytest.fixture
def create_png_data_format(db):
    """create a png dataformat instance"""
    data_format_details = {
        "name": "png",
    }
    data_format = DataFormat.objects.create(**data_format_details)
    data_format.save()
    return data_format


@pytest.fixture
def create_output_file(create_service, create_data_format):
    """create a service instance"""
    output_file = OutputFile()
    output_file.data_format = create_data_format
    output_file.service = create_service
    output_file.name = "Output file"
    output_file.save()
    return output_file


@pytest.fixture
def create_parameter_option(db):
    """create a parameter option instance"""
    parameter_option = ParameterOption()
    parameter_option.short_name = "Parameter option"
    parameter_option.save()
    return parameter_option


@pytest.fixture
def create_parameter_template(
    create_service, create_png_data_format, create_parameter_option
):
    """create a parameter template instance"""
    parameter_template = ParameterTemplate()
    parameter_template.name = "Image"
    parameter_template.service = create_service
    parameter_template.data_format = create_png_data_format
    parameter_template.parameter_option = create_parameter_option
    parameter_template.save()
    return parameter_template
