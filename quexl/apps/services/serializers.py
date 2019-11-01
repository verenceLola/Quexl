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


class ServicesSerializer(serializers.ModelSerializer):
    """
    serializer for the services model
    """

    class Meta:
        model = Service
        exclude = ("price_currency",)

    price = PriceSerializer(source=("priceInfo"))
    category = CategorySerializer()


class OrdersSerializer(serializers.ModelSerializer):
    """
    serializer for services orders
    """

    class Meta:
        model = Order
        exclude = ("amount", "amount_currency")

    price = PriceSerializer(source=("priceInfo"))
    buyer = UserSerializer()
    seller = UserSerializer()


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
