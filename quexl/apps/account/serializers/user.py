from typing import Dict

from rest_framework import serializers

from quexl.apps.account.models import User

from .permissions import GroupSerializer
from .permissions import PermissionsSerializer


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

    def update(self, instance: User, validated_data: Dict[str, str]) -> User:
        """Performs an update on a User."""
        password = validated_data.pop("password", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
            "updated_at",
            "groups",
        )

    is_admin = serializers.BooleanField(source="is_superuser", read_only=True)
    user_permissions = PermissionsSerializer(many=True)
    roles = GroupSerializer(many=True, source="groups")
