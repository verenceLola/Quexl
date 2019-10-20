from rest_framework import serializers


class RolesSerializer(serializers.Serializer):
    """
    serialize roles data
    """

    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_name(self, obj):
        """
        get role name
        """
        return obj.get_name()

    def get_description(self, obj):
        """
        get role description
        """
        return obj.get_description()
