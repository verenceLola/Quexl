from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    serializer for user info
    """

    class Meta:
        fields = ("email", "username", "id")
        model = get_user_model()
