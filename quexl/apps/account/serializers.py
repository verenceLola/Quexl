from django.contrib.auth import authenticate

from rest_framework import serializers, validators
from rest_framework.validators import UniqueValidator

from quexl.apps.account.backends import JWTAuthentication
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    def __init__(self, *args, **kwargs):
        super(RegistrationSerializer, self).__init__(*args, **kwargs)

        # Override the default error_messages with a custom field error
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

    # Ensure that username is unique, does not exist,
    #  cannot be left be blank, has a minimum of 5 characters
    # has alphanumerics only
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

    # Ensure passwords are at least 8 characters long,
    # at least one letter and at least one number
    password = serializers.RegexField(
        regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{7,}$",
        max_length=128,
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

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """The class to serialize login details"""

    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        """
        validate details
        """
        user = data.get("email", None)  # get user object as key 'email'
        email = user.email
        password = data.get("password", None)
        if not password:
            raise serializers.ValidationError(
                "Kindly enter your password to log in."
            )

        auth_user = authenticate(email=email, password=password)

        if not user.is_active:
            raise serializers.ValidationError(
                "Your account is inactive. Kindly check your email for an "
                "activation link to activate "
            )
        if auth_user is None:
            raise serializers.ValidationError(
                {
                    "password": "Password isn’t right. Double check "
                    ", or reset your password to log in. "
                }
            )

        token = JWTAuthentication.generate_token(email)

        return {"email": user.email, "username": user.username, "token": token}

    def validate_email(self, value):
        """
        validate user password
        """
        user = User.get_user(value)
        if not user:
            raise serializers.ValidationError(
                f"User with email {value} not found."
            )
        return user  # return user object to reduce unnecessary db queries


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for forget password"""

    email = serializers.CharField(max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for reset password"""

    class Meta:
        model = User
        fields = ("password",)


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters.
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True
    )

    class Meta:
        model = User
        fields = ("email", "username", "password")

    def update(self, instance, validated_data):
        """Performs an update on a User."""
        password = validated_data.pop("password", None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class SocialAuthSerializer(serializers.Serializer):
    """ Accepts provider, access token , and access_token_secret"""

    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(
        max_length=4096, required=True, trim_whitespace=True
    )
    access_token_secret = serializers.CharField(
        max_length=4096, required=False, trim_whitespace=True
    )
