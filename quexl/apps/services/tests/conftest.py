"""configure common testing methods"""
import os

import pytest
from django.core.files import File

from quexl.apps.services.models import Category
from quexl.apps.services.models import DataFormat
from quexl.apps.services.models import Gallery
from quexl.apps.services.models import OutputFile
from quexl.apps.services.models import ParamerterOption
from quexl.apps.services.models import ParamerterTemplate
from quexl.apps.services.models import Service


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
def create_service(create_category, create_db_user):
    """create a service instance"""
    service = Service()
    service.name = "Service 1"
    service.delivery_time = "2070-11-01 21:40:53.028781+03"
    service.category_id = create_category.id
    service.price.amount = "999"
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
def create_output_file(create_service, create_data_format):
    """create a service instance"""
    output_file = OutputFile()
    output_file.data_format = create_data_format
    output_file.service = create_service
    output_file.name = "Output file"
    output_file.save()
    return output_file


@pytest.fixture
def create_parameter_template(create_service, create_data_format):
    """create a parameter template instance"""
    parameter_template = ParamerterTemplate()
    parameter_template.name = "Parameter template"
    parameter_template.service = create_service
    parameter_template.data_format = create_data_format
    parameter_template.save()
    return parameter_template


@pytest.fixture
def create_parameter_option(create_parameter_template):
    """create a parameter option instance"""
    parameter_option = ParamerterOption()
    parameter_option.short_name = "Parameter option"
    parameter_option.data_format = create_data_format
    parameter_option.parameter = create_parameter_template
    parameter_option.save()
    return parameter_option
