from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rolepermissions.checkers import has_permission
from rolepermissions.exceptions import RoleDoesNotExist
from rolepermissions.roles import assign_role
from rolepermissions.roles import get_user_roles
from rolepermissions.roles import remove_role

from quexl.helpers.api_response import APIResponse

from ..serializers import RolesSerializer


class UserRoleAPIView(GenericAPIView):
    """
    manage user roles
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = RolesSerializer

    def post(self, request, user_id):
        """
        assign user roles
        """
        role = request.data.get("role", None)
        self.operation = "Assign user role"  # specify view operation

        if not role:
            return Response(
                {
                    "message": "%s failed" % self.operation,
                    "error": "Missing role field",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            if has_permission(request.user, "assign_user_roles"):
                user = get_user_model().objects.get(id=user_id)
                new_role = assign_role(user, role)
                serializer = self.serializer_class(new_role)

                return APIResponse.get_success_responses(
                    "User assigned %s role successfully" % role,
                    serializer.data,
                    status_code=status.HTTP_201_CREATED,
                )
            else:
                return APIResponse.get_error_response(
                    "%s failed" % self.operation,
                    "You don't have permission to assign roles",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
        except get_user_model().DoesNotExist:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except RoleDoesNotExist:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "Role named %s does not exist" % role,
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def get(self, request, user_id):
        """"
        get user roles
        """
        self.operation = "View user roles"
        try:
            if has_permission(request.user, "view_user_roles"):
                user = get_user_model().objects.get(id=user_id)
                user_roles = get_user_roles(user)
                serializer = self.serializer_class(user_roles, many=True)

                return (
                    APIResponse.get_success_responses(
                        "User has the following roles",
                        serializer.data,
                        status_code=status.HTTP_200_OK,
                    )
                    if len(serializer.data) > 0
                    else APIResponse.get_error_response(
                        "%s failed" % self.operation,
                        "User does not have any roles",
                        status_code=status.HTTP_200_OK,
                    )
                )
            else:
                user = request.user
                user_roles = get_user_roles(user)
                serializer = self.serializer_class(user_roles, many=True)

                return (
                    APIResponse.get_success_responses(
                        "You have the following roles",
                        serializer.data,
                        status_code=status.HTTP_200_OK,
                    )
                    if len(serializer.data) > 0
                    else APIResponse.get_error_response(
                        "%s failed" % self.operation,
                        "You don't have any roles",
                        status_code=status.HTTP_200_OK,
                    )
                )

        except get_user_model().DoesNotExist:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, user_id):
        """
        remove user role
        """
        role = request.data.get("role", None)
        self.operation = "Remove user role"

        if not role:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "Missing role field",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            if has_permission(request.user, "remove_user_roles"):
                user = get_user_model().objects.get(id=user_id)
                revoked_role = remove_role(user, role)
                serializer = self.serializer_class(revoked_role)

                return APIResponse.get_success_responses(
                    "User role %s removed successfully" % role,
                    serializer.data,
                    status_code=status.HTTP_200_OK,
                )
            else:
                return APIResponse.get_error_response(
                    "%s failed" % self.operation,
                    "You don't have permission to remove user roles",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
        except get_user_model().DoesNotExist:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except RoleDoesNotExist:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "Role named %s does not exist" % role,
                status_code=status.HTTP_404_NOT_FOUND,
            )
