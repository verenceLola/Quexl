# config tests file
import os

import pytest
from django.core.files import File

# models
from quexl.apps.orders.models import DataFile
from quexl.apps.orders.models import History
from quexl.apps.orders.models import Order
from quexl.apps.orders.models import Parameter


@pytest.fixture
def create_data_file(create_jpg_data_format):
    """create a datafile instance"""
    if not os.path.exists("./test_files"):
        os.mkdir("./test_files")
    im = open("./test_files/img.jpg", "w")
    image_file = File(im)
    data_file = DataFile()
    data_file.data_format = create_jpg_data_format
    data_file.data_file_upload = image_file.file.name
    data_file.name = "Image file"
    data_file.save()
    if os.path.exists("./test_files"):
        if os.path.exists("./test_files/img.jpg"):
            os.remove("./test_files/img.jpg")
        os.rmdir("./test_files")
    return data_file


@pytest.fixture
def create_parameter(create_parameter_template):
    """create a parameter instance"""
    parameter = Parameter()
    parameter.parameter_template = create_parameter_template
    parameter.comment = "jpg_to_png"
    parameter.save()
    return parameter


@pytest.fixture
def create_history_element(create_data_file):
    """create an order instance"""
    hist = History()
    hist.set(data_file=create_data_file)
    hist.output_url = "https://sandbox.zamzar.com/v1/jobs/id"
    hist.save()
    return hist


@pytest.fixture
def create_order(
    create_service,
    create_parameter,
    create_data_file,
    create_db_user,
    create_history_element,
):
    """create an order instance"""
    order = Order()
    order.service = create_service
    order.parameter = create_parameter
    order.data_file = create_data_file
    order.history = create_data_file
    order.status = "PROCESSING"
    order.price.amount = "5"
    order.price.currency = "usd"
    order.buyer = create_db_user
    order.save()
    return order
