from django.db import models
from django.utils.text import slugify
from djmoney.models.fields import MoneyField
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey

from quexl.apps.account.models import User
from quexl.helpers.fancy_generator import fancy_id_generator

WEB_FORM_CHOICES = [
    ("text_field", "Text field"),
    ("text_area", "Text area"),
    ("radio_button", "Radio button"),
    ("checkbox", "Checkbox"),
]


class Category(MPTTModel):
    """
    category model
    """

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=20, unique=True)
    parent = TreeForeignKey(
        "self",
        db_constraint=True,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ("name",)

    class Meta:
        unique_together = ("parent", "name")
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        """
        generate category slug from category name
        """
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class DataFormat(models.Model):
    """Data format model"""

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True)


class Service(models.Model):
    """
    services model
    """

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(unique=True, max_length=100)
    api_endpoint = models.CharField(max_length=150)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=True)
    price = MoneyField(
        max_digits=19, decimal_places=4, default=0.0000, default_currency="USD"
    )
    delivery_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = TreeForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )
    is_published = models.BooleanField(default=False)
    sub_category = models.CharField(max_length=150, blank=True)
    long_description = models.TextField(blank=True)


class Gallery(models.Model):
    """Gallery model"""

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    description = models.CharField(max_length=200)


class OutputFile(models.Model):
    """Output file model"""

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE)


class ParameterOption(models.Model):
    """
    Parameter option model
    """

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    short_name = models.CharField(max_length=200)
    option_text = models.CharField(blank=True, max_length=200)
    price = MoneyField(
        max_digits=19, decimal_places=4, default=0.0000, default_currency="USD"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ParameterTemplate(models.Model):
    """
    Parameter Template model
    """

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    parameter_option = models.ForeignKey(
        ParameterOption, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    web_form = models.CharField(
        max_length=10, choices=WEB_FORM_CHOICES, default="text_field"
    )
    cols_min = models.IntegerField(default=0)
    rows_min = models.IntegerField(default=0)
    from_history = models.BooleanField(default=False)
    from_from_field = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
