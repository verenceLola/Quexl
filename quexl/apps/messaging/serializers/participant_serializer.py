from django.contrib.auth import get_user_model
from rest_framework import serializers


class ParticipantSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField(read_only=True)

    def validate_username(self, value):
        """
        ensure the specified username exists
        """
        try:
            get_user_model().objects.get(username=value)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(
                f"User with username {value} doesn't exist"
            )
        return value
