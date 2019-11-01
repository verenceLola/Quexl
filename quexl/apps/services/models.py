from django.db import models
from quexl.helpers.fancy_generator import fancy_id_generator
from djmoney.models.fields import MoneyField
from quexl.apps.account.models import User
from django.contrib.postgres.fields import ArrayField
from mptt.models import TreeForeignKey, MPTTModel
from django.utils.text import slugify


STATUS_CHOICES = [
    ("started", "order started"),
    ("canceled", "order canceled"),
    ("delivered", "order delivered"),
    ("accepted", "order accepted"),
    ("completed", "order completed"),
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
    name = models.CharField(max_length=20)
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

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        generate category slug from category name
        """
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Service(models.Model):
    """
    services model
    """

    class Meta:
        verbose_name_plural = "services"
        unique_together = ("name", "seller")

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(max_length=300)
    price = MoneyField(
        max_digits=19, decimal_places=4, default=0.0000, default_currency="USD"
    )
    delivery_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="service_seller"
    )
    category = TreeForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    order services model
    """

    class Meta:
        verbose_name_plural = "orders"

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="order_seller"
    )
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="order_buyer"
    )
    price = MoneyField(
        max_digits=19, decimal_places=4, default=0.0000, default_currency="USD"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_ending = models.DateTimeField()
    number_of_revisions = models.PositiveIntegerField(
        default=0
    )  # max of 5 revisions
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="started"
    )
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    description = models.TextField(max_length=300)
    order_type = models.CharField(
        max_length=10,
        choices=[("offer", "order offer"), ("proposal", "order proposal")],
        default="offer",  # default value when selling service
    )
    attachment = ArrayField(
        models.URLField(null=True), size=5, default=list
    )  # allow a maximum of 5 attachments
    details = models.TextField(
        max_length=300
    )  # describe buyer_requirements if buying, or seller_deliverable when selling
    # seller_deliverables = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return self.description


class Request(models.Model):
    """
    service requests
    """

    class Meta:
        verbose_name_plural = "requests"

    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    category = TreeForeignKey(
        "Category", on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField(max_length=300)
    price = MoneyField(
        max_digits=19, decimal_places=4, default=0.0000, default_currency="USD"
    )
    delivery_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    buyer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="request_buyer"
    )
    date_created = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    attached_files = ArrayField(models.URLField(), size=5)

    @property
    def priceInfo(self):
        """
        return price info: amount & currency
        """
        return self.price

    def __str__(self):
        return self.description


class Payment(models.Model):
    """
    order payments model
    """

    VERIFIED = "Verified"
    CANCELED = "Canceled"
    PAYMENT_STATUS = [(VERIFIED, "verified"), (CANCELED, "canceled")]
    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    buyer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="paid_by"
    )
    issued_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=20)
    amount = MoneyField(
        max_digits=19, decimal_places=4, default=0.0000, default_currency="USD"
    )
    seller = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="paid_to"
    )
    payment_code = models.CharField(
        editable=False, default=fancy_id_generator, max_length=256
    )
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS)

    def __str__(self):
        # import pdb; pdb.set_trace()
        return "%s %s" % (self.amount.currency, self.amount.amount.__str__())

    @property
    def priceInfo(self):
        """
        return price amount and currency
        """
        return self.amount
