from django_countries import countries
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class CountrySerializerWrapper(serializers.ModelSerializer):
    """
    wrapper for related fields serializers
    """

    def validate_country(self, value: str) -> str:
        """
        validate country code
        """
        if countries.countries.get(value.upper()):

            return value.upper()

        raise ValidationError("%s is not a valid country code" % value)
