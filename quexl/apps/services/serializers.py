"""
Service serializers
"""
from datetime import datetime

from djmoney.money import DefaultMoney
from moneyed.classes import CurrencyDoesNotExist
from mptt.exceptions import InvalidMove
from pytz import UTC
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# local imports
from quexl.apps.services.models import Category
from quexl.apps.services.models import DataFormat
from quexl.apps.services.models import Gallery
from quexl.apps.services.models import OutputFile
from quexl.apps.services.models import ParameterOption
from quexl.apps.services.models import ParameterTemplate
from quexl.apps.services.models import Service


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

    def validate_price(self, value):  # pragma: no cover
        """
        validate price
        """
        priceInfo = self.initial_data.get("price") or self.initial_data.get(
            "amount"
        )
        try:
            if int(priceInfo["amount"]) < 0:
                raise ValidationError("Amount cannot be less than zero")
            money = DefaultMoney(
                amount=priceInfo["amount"], currency=priceInfo["currency"]
            )
        except CurrencyDoesNotExist:
            raise ValidationError("Currency does not exist")
        except KeyError:
            raise ValidationError("Missing amount or currency info")
        except ValueError:
            raise ValidationError("Amount should be a positive integer")
        return money


class CategorySerializer(serializers.ModelSerializer):
    """
    serializer for catergory model
    """

    class Meta:
        model = Category
        exclude = ("lft", "rght", "tree_id", "level", "parent")

    name = serializers.CharField(max_length=200)
    slug = serializers.SlugField(read_only=True)
    parent_id = serializers.CharField(required=False, write_only=True)
    sub_categories = serializers.SerializerMethodField()

    def get_sub_categories(self, parent):
        queryset = parent.get_children()
        serializer = CategorySerializer(
            queryset, many=True, context=self.context
        )
        return serializer.data

    def create(
        self, validated_data
    ):  # TODO: fix permissions to ensure that only users with rewuired permissions can create a new category.  # noqa
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
                    return {"parent": parent, "name": name}
            except Category.DoesNotExist:
                raise ValidationError(
                    {
                        "parent_id": "Category with id %s does not exist"
                        % parent_id
                    }
                )
        else:
            if Category.objects.filter(name=name):
                raise ValidationError(
                    {"name": "Catergory with that name already exists"}
                )
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
                {
                    "name": "A category cannot be a \
                        sub-category of one of its sub-categories"
                }
            )
        return instance


class ServicesSerializer(PriceSerializerWrapper):
    """
    serializer for the services model
    """

    class Meta:
        model = Service
        fields = "__all__"
        read_only_fields = ("category", "seller", "created_at", "updated_at")

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


class ParameterTemplateSerializer(serializers.ModelSerializer):
    """
    serializer for the Parameter template model
    """

    class Meta:
        model = ParameterTemplate
        fields = "__all__"


class ParameterOptionSerializer(PriceSerializerWrapper):
    """
    serializer for the parameter option model
    """

    class Meta:
        model = ParameterOption
        fields = "__all__"


class DataFormatSerializer(serializers.ModelSerializer):
    """
    serializer for the services model
    """

    class Meta:
        model = DataFormat
        fields = "__all__"


class OutputFileSerializer(serializers.ModelSerializer):
    """
    Output file serializer class
    """

    class Meta:
        model = OutputFile
        fields = "__all__"


class GallerySerializer(serializers.ModelSerializer):
    """
    Gallery serializer class
    """

    class Meta:
        model = Gallery
        fields = "__all__"
