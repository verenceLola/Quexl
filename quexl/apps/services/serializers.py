"""
services serializers
"""
from rest_framework import serializers
from quexl.apps.services.models import (
    Service,
    Category,
    Order,
    Request,
    Payment,
)
from quexl.apps.account.serializers import UserSerializer
from rest_framework.validators import ValidationError
from mptt.exceptions import InvalidMove
from datetime import datetime
from pytz import UTC
from rest_framework.exceptions import PermissionDenied
from djmoney.money import DefaultMoney
from moneyed.classes import CurrencyDoesNotExist
from rolepermissions.checkers import has_permission


class PriceSerializer(serializers.Serializer):
    """
    serializer for price objects
    """

    amount = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    def get_amount(self, obj):
        """
        return price amount
        """
        return obj.amount.__str__()

    def get_currency(self, obj):
        """
        get price currency
        """
        return obj.currency.__str__()


class PriceSerializerWrapper(serializers.ModelSerializer):
    """
    wrapper for price serializer and methods
    """

    price = PriceSerializer()

    def validate_price(self, value):
        """
        validate price info
        """
        priceInfo = self.initial_data["price"]
        try:
            money = DefaultMoney(
                amount=priceInfo["amount"], currency=priceInfo["currency"]
            )
        except CurrencyDoesNotExist:
            raise ValidationError("Currency does not exist")
        return money


class CategorySerializer(serializers.ModelSerializer):
    """
    serializer for catergory model
    """

    class Meta:
        model = Category
        exclude = ("lft", "rght", "tree_id", "level", "parent")

    name = serializers.CharField()
    slug = serializers.SlugField(read_only=True)
    parent_id = serializers.CharField(required=False, write_only=True)
    sub_categories = serializers.SerializerMethodField()

    def get_sub_categories(self, parent):
        queryset = parent.get_children()
        serializer = CategorySerializer(
            queryset, many=True, context=self.context
        )
        return serializer.data

    def create(self, validated_data):
        """
        create new category instance
        """
        name = validated_data.pop("name")
        parent = validated_data.get("parent", None)
        return Category.objects.create(parent=parent, name=name)

    def validate(self, data):
        """
        validate category data
        """
        parent_id = data.get("parent_id", None)
        name = data.get("name")
        if parent_id:
            try:
                parent = Category.objects.get(id=parent_id)
                if Category.objects.filter(parent_id=parent_id, name=name):
                    raise ValidationError({"name": "Catergory already exists"})
                else:
                    return {"parent": parent, "category_name": name}
            except Category.DoesNotExist:
                raise ValidationError(
                    {
                        "parent_id": "Category with id %s does not exist"
                        % parent_id
                    }
                )
        else:
            if Category.objects.filter(name=name):
                raise ValidationError({"name": "Catergory already exists"})
            else:
                return {"name": name}

    def update(self, instance, validated_data):
        """
        update category details
        """
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        try:
            instance.save()
        except InvalidMove:
            raise ValidationError(
                "A category cannot be a sub-category of one of its sub-categories"
            )
        return instance


class ServicesSerializer(PriceSerializerWrapper):
    """
    serializer for the services model
    """

    class Meta:
        model = Service
        exclude = ("price_currency",)

    category = CategorySerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    category_id = serializers.CharField(write_only=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        """
        validate service data
        """
        category_id = data.get("category_id", None)
        if category_id:
            try:
                category = Category.objects.get(pk=category_id)
                data.update({"category": category})
            except Category.DoesNotExist:
                raise ValidationError(
                    "Category with id %s does not exist" % category_id
                )
        return data

    def validate_name(self, value):
        """
        validate user doesn't have service with same name
        """
        if Service.objects.filter(name=value):
            raise ValidationError(
                "service with '%s' name elready exists" % value
            )
        return value

    def create(self, validated_data):
        """
        create a service with seller as the current user
        """
        validated_data.update({"seller": self.context["request"].user})
        service = Service.objects.create(**validated_data)
        return service

    def validate_delivery_time(self, value):
        """
        ensure delivery time is a future date
        """
        if datetime.utcnow().replace(tzinfo=UTC) > value:
            raise ValidationError("Delivery time cannot be a past date")
        return value


class OrdersSerializer(PriceSerializerWrapper):
    """
    serializer for services orders
    """

    class Meta:
        model = Order
        exclude = ("price_currency", "service")

    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    service_id = serializers.ReadOnlyField()
    order_type = serializers.ReadOnlyField()

    def create(self, validated_data):
        """
        create new order
        """
        service_id = self.context["view"].kwargs["service_id"]
        if Order.objects.filter(service_id=service_id):
            raise ValidationError("Order already exists. Kindly update")
        service = Service.objects.get(id=service_id)
        validated_data.pop(
            "status", None
        )  # prevent creating order with status set
        buyer = self.context["request"].user
        seller = service.seller
        return Order.objects.create(
            service=service, buyer=buyer, seller=seller, **validated_data
        )

    def validate_date_ending(self, value):
        """
        ensure ending time is a future date
        """
        if datetime.utcnow().replace(tzinfo=UTC) > value:
            raise ValidationError("Ending date cannot be a past date")
        return value

    def validate_number_of_revisions(self, value):
        """
        ensure the number of revisions is less than or equal to 5
        """
        if value <= 5:
            return value
        raise ValidationError(
            "Number of revision should be between less than or equal to 5"
        )

    def validate_attachment(self, value):
        """
        ensure unique urls added as attachment
        """
        attachments = set(value)  # prevent adding duplicate attachment urls
        return list(attachments)

    def update(self, instance, validated_data):
        """
        validate order details
        """
        status = validated_data.pop("status", None)
        if status and not has_permission(
            self.context["request"].user, "edit_order_status"
        ):
            raise PermissionDenied(
                "Only users with required permissions can edit order status"
            )
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class ServiceRequestSerializer(serializers.ModelSerializer):
    """
    serialize service request data
    """

    class Meta:
        model = Request
        exclude = ("price_currency",)

    price = PriceSerializer(source="priceInfo")
    category = CategorySerializer()
    buyer = UserSerializer()


class PaymentSerializer(serializers.ModelSerializer):
    """
    serialize order payment data
    """

    class Meta:
        model = Payment
        exclude = ("amount", "amount_currency")

    paid = PriceSerializer(source="priceInfo")
    order = OrdersSerializer()
    seller = UserSerializer()
    buyer = UserSerializer()
