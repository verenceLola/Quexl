from django.contrib.auth.models import Group, Permission
from rest_framework import serializers


class PermissionsSerializer(serializers.ModelSerializer):
    """
    serialize user permissions
    """

    class Meta:
        model = Permission
        exclude = ("content_type",)


class GroupSerializer(serializers.ModelSerializer):
    """
    serialize user groups
    """

    class Meta:
        model = Group
        exclude = ("permissions",)
