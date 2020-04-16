from typing import Dict

from rest_framework import serializers
from rest_framework import validators
from rest_framework.validators import UniqueValidator

from quexl.apps.account.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    def __init__(self, *args, **kwargs) -> None:
        super(RegistrationSerializer, self).__init__(*args, **kwargs)

        for field in self.fields:
            error_messages = self.fields[field].error_messages
            error_messages["null"] = error_messages["blank"] = error_messages[
                "required"
            ] = "Please fill in the {}.".format(field)

    email = serializers.RegexField(
        regex=r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$",
        validators=[
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message="Email address already exists",
            )
        ],
        error_messages={"invalid": "Enter a valid email address"},
    )
    username = serializers.RegexField(
        regex=r"^[A-Za-z\-\_]+\d*$",
        min_length=4,
        max_length=30,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="The username already exists. Kindly try another.",
            )
        ],
        error_messages={
            "min_length": "Username must have a minimum of 4 characters.",
            "max_length": "Username must have a maximum of 30 characters.",
            "invalid": "Username cannot only have alphanumeric characters.",
        },
    )
    password = serializers.RegexField(
        regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{7,}$",
        max_length=128,
        min_length=7,
        write_only=True,
        error_messages={
            "required": "Password is required",
            "max_length": "Password cannot be more than 128 characters",
            "min_length": "Password must have at least 7 characters",
            "invalid": "Password must have a number and a letter",
        },
    )
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ["email", "username", "password", "token"]

    def create(self, validated_data: Dict[str, str]) -> User:
        # Use the `create_user` method we wrote earlier to create a new user.
        user = User.objects.create_user(**validated_data)

        return user
