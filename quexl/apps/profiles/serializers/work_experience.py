from collections import OrderedDict
from datetime import datetime
from typing import Dict
from typing import Union

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from quexl.apps.profiles.models import Profile
from quexl.apps.profiles.models import WorkExperience

from .country_serializer_wrapper import CountrySerializerWrapper


class WorkExperienceSerializer(CountrySerializerWrapper):
    """
    work experience serializer
    """

    class Meta:
        exclude = ("profile", "id")
        model = WorkExperience

    description = serializers.CharField(required=True)
    on_going = serializers.BooleanField(read_only=True)
    employee = serializers.CharField(required=True)
    start_date = serializers.DateTimeField(required=True)
    end_date = serializers.DateTimeField(required=True)
    country = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    def create(
        self, validated_data: Dict[str, Union[str, datetime, Profile]]
    ) -> WorkExperience:
        """
        create user work experience
        """
        employee = validated_data.pop("employee")
        role = validated_data.pop("role")
        profile = validated_data.pop("profile")
        work, _ = WorkExperience.objects.get_or_create(
            employee=employee, role=role, profile=profile
        )
        work.start_date = validated_data["start_date"]
        work.end_date = validated_data["end_date"]
        work.description = validated_data["description"]
        work.country = validated_data["country"]
        work.save()

        return work

    def validate_start_date(self, value: datetime) -> datetime:
        """
        validate work start date
        """
        if value > timezone.now():  # start_date is future date
            raise ValidationError("Start date cannot be a future date")

        return value

    def validate(self, data: dict) -> OrderedDict:
        """
        validate work experience data
        """
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)

        if not start_date or not end_date:
            return super(WorkExperienceSerializer, self).validate(data)

        if start_date > end_date:  # start_date cannot be later than end_date
            raise ValidationError(
                {"end_date": "End date cannot be earlier than the start date"}
            )

        return data
