from typing import Type
from typing import Union

from rest_framework import serializers

from quexl.apps.roles.roles import DeveloperRole
from quexl.apps.roles.roles import RegularUserRole


class RolesSerializer(serializers.Serializer):
    """
    serialize roles data
    """

    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_name(
        self, obj: Union[Type[RegularUserRole], Type[DeveloperRole]]
    ) -> str:
        """
        get role name
        """

        return obj.get_name()

    def get_description(
        self, obj: Union[Type[RegularUserRole], Type[DeveloperRole]]
    ) -> str:
        """
        get role description
        """

        return obj.get_description()
