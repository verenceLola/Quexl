from django.db import models
from djmoney.models.fields import MoneyField

from quexl.apps.account.models import User
from quexl.apps.services.models import DataFormat
from quexl.apps.services.models import ParameterTemplate
from quexl.apps.services.models import Service
from quexl.helpers.fancy_generator import fancy_id_generator

ORDER_STATUS = (
    ("PROCESSING", "processing"),
    ("CANCELLED", "cancelled"),
    ("COMPLETED", "completed"),
)


class DataFile(models.Model):
    """Datafile model"""

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE)
    data_file_upload = models.FileField(upload_to="uploads/")
    file_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Parameter(models.Model):
    """parameter model"""

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    comment = models.TextField(blank=True)
    content = models.CharField(max_length=300, blank=True)
    parameter_template = models.ForeignKey(
        ParameterTemplate, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class History(models.Model):
    """history model"""

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    output_url = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    data_file = models.ManyToManyField(DataFile)
    history_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    """order model"""

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    job_id = models.CharField(max_length=256)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    history = models.OneToOneField(History, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    end_date = models.DateTimeField(blank=True)
    ordered = models.BooleanField(default=False)
    custom = models.BooleanField(default=False)
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE, blank=True, null=True
    )
    data_file = models.ForeignKey(DataFile, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50, choices=ORDER_STATUS, default="processing"
    )
    price = MoneyField(
        max_digits=19, decimal_places=4, default=0.0000, default_currency="USD"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
