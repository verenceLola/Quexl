from typing import Dict
from typing import Union

from django.core.validators import RegexValidator
from phonenumber_field.validators import validate_international_phonenumber
from rest_framework import serializers

from quexl.apps.profiles.models import Address
from quexl.apps.profiles.models import Profile

from .country_serializer_wrapper import CountrySerializerWrapper


class AddressSerializer(CountrySerializerWrapper):
    """
    address serializer
    """

    class Meta:
        exclude = ("profile", "id")
        model = Address

    street_address_1 = serializers.CharField(required=True)
    city = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                r"^[A-Za-z]+$",
                message="value should be string characters only",
            )
        ],
    )
    city_area = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                r"^[A-Za-z]+$",
                message="value should be string characters only",
            )
        ],
    )
    postal_code = serializers.IntegerField(required=True)
    country = serializers.CharField(required=True)
    country_area = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                r"^[A-Za-z]+$",
                message="value should be string characters only",
            )
        ],
    )
    phone = serializers.CharField(
        required=True, validators=[validate_international_phonenumber]
    )

    def create(
        self, validated_data: Dict[str, Union[str, int, Profile]]
    ) -> Address:
        """
        create user address info
        """
        address, _ = Address.objects.get_or_create(
            **validated_data
        )  # prevent creating similar address info

        return address
