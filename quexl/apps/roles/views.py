from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rolepermissions.roles import get_user_roles, assign_role, remove_role
from rolepermissions.checkers import has_permission
from rolepermissions.exceptions import (
    RoleDoesNotExist,
    RolePermissionScopeException,
)
from rest_framework import status
from django.contrib.auth import get_user_model
from quexl.helpers.endpoint_response import (
    get_success_responses,
    get_error_response,
)
from quexl.apps.roles.serializers import RolesSerializer
from rolepermissions.permissions import (
    available_perm_status,
    grant_permission,
    revoke_permission,
)


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
        if not role:
            return get_error_response(
                "Missing role field", status_code=status.HTTP_400_BAD_REQUEST
            )
        try:
            if has_permission(request.user, "assign_user_roles"):
                user = get_user_model().objects.get(id=user_id)
                new_role = assign_role(user, role)
                serializer = self.serializer_class(new_role)
                return get_success_responses(
                    "User assigned %s role successfully" % role,
                    serializer.data,
                    status_code=status.HTTP_201_CREATED,
                )
            else:
                return get_error_response(
                    "You don't have permission to assign roles",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
        except get_user_model().DoesNotExist:
            return get_error_response(
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except RoleDoesNotExist:
            return get_error_response(
                "Role named %s does not exist" % role,
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def get(self, request, user_id):
        """"
        get user roles
        """
        try:
            if has_permission(request.user, "view_user_roles"):
                user = get_user_model().objects.get(id=user_id)
                user_roles = get_user_roles(user)
                serializer = self.serializer_class(user_roles, many=True)
                return (
                    get_success_responses(
                        "User has the following roles",
                        serializer.data,
                        status_code=status.HTTP_200_OK,
                    )
                    if len(serializer.data) > 0
                    else get_error_response(
                        "User does not have any roles",
                        status_code=status.HTTP_200_OK,
                    )
                )
            else:
                user = request.user
                user_roles = get_user_roles(user)
                serializer = self.serializer_class(user_roles, many=True)
                return (
                    get_success_responses(
                        "You have the following roles",
                        serializer.data,
                        status_code=status.HTTP_200_OK,
                    )
                    if len(serializer.data) > 0
                    else get_error_response(
                        "You don't have any roles",
                        status_code=status.HTTP_200_OK,
                    )
                )

        except get_user_model().DoesNotExist:
            return get_error_response(
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request, user_id):
        """
        remove user role
        """
        role = request.data.get("role", None)
        if not role:
            return get_error_response(
                "Missing role field", status_code=status.HTTP_400_BAD_REQUEST
            )
        try:
            if has_permission(request.user, "remove_user_roles"):
                user = get_user_model().objects.get(id=user_id)
                revoked_role = remove_role(user, role)
                serializer = self.serializer_class(revoked_role)
                return get_success_responses(
                    "User role %s removed successfully" % role,
                    serializer.data,
                    status_code=status.HTTP_200_OK,
                )
            else:
                return get_error_response(
                    "You don't have permission to remove user roles",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
        except get_user_model().DoesNotExist:
            return get_error_response(
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except RoleDoesNotExist:
            return get_error_response(
                "Role named %s does not exist" % role,
                status_code=status.HTTP_404_NOT_FOUND,
            )


class PermissionsAPIView(GenericAPIView):
    """
    manage user permissions
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        """
        get user permissions
        """
        try:
            if has_permission(request.user, "view_user_permissions"):
                user = get_user_model().objects.get(id=user_id)
                perms = available_perm_status(user)
                return (
                    get_success_responses(
                        "User has the following permmissions",
                        perms,
                        status_code=status.HTTP_200_OK,
                    )
                    if perms
                    else get_error_response(
                        "User does not have any permissions assigned",
                        status_code=status.HTTP_200_OK,
                    )
                )
            else:
                perms = available_perm_status(request.user)
                return (
                    get_success_responses(
                        "You have the following permissions",
                        perms,
                        status_code=status.HTTP_200_OK,
                    )
                    if perms
                    else get_error_response(
                        "You don't have any permissions",
                        status_code=status.HTTP_200_OK,
                    )
                )
        except get_user_model().DoesNotExist:
            return get_error_response(
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, user_id):
        """
        assign user permissions
        """
        permission = request.data.get("permission")
        if not permission:
            return get_error_response(
                "Missing permission field",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            if has_permission(request.user, "assign_user_permission"):
                user = get_user_model().objects.get(id=user_id)
                grant_permission(user, permission)
                return get_success_responses(
                    "User assigned %s permission successfully" % permission,
                    {"permission_assigned": permission},
                    status_code=status.HTTP_201_CREATED,
                )
            else:
                return get_error_response(
                    "You do not have permission to assign user permissions",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
        except get_user_model().DoesNotExist:
            return get_error_response(
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except RolePermissionScopeException:
            return get_error_response(
                "User missing required role(s) for %s permission" % permission,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, user_id):
        """
        revoke user permissions
        """
        permission = request.data.get("permission")
        if not permission:
            return get_error_response(
                "Missing permission field",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            if has_permission(request.user, "revoke_user_permissions"):
                user = get_user_model().objects.get(id=user_id)
                revoke_permission(user, permission)
                return get_success_responses(
                    "user permission revoked successfully",
                    {"permission_revoked": permission},
                    status_code=status.HTTP_200_OK,
                )
            else:
                return get_error_response(
                    "You do not have permission to revoke user permissions",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
        except get_user_model().DoesNotExist:
            return get_error_response(
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except RolePermissionScopeException:
            return get_error_response(
                "User missing required role(s) for %s permission" % permission,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
