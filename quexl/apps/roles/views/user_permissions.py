from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rolepermissions.checkers import has_permission
from rolepermissions.exceptions import RolePermissionScopeException
from rolepermissions.permissions import available_perm_status
from rolepermissions.permissions import grant_permission
from rolepermissions.permissions import revoke_permission

from quexl.helpers.api_response import APIResponse


class PermissionsAPIView(GenericAPIView):
    """
    manage user permissions
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        """
        get user permissions
        """
        self.operation = "View user permissions"  # specify view operation

        try:
            if has_permission(request.user, "view_user_permissions"):
                user = get_user_model().objects.get(id=user_id)
                perms = available_perm_status(user)

                return (
                    APIResponse.get_success_responses(
                        "User has the following permmissions",
                        perms,
                        status_code=status.HTTP_200_OK,
                    )
                    if perms
                    else APIResponse.get_error_response(
                        "%s failed" % self.operation,
                        "User does not have any permissions assigned",
                        status_code=status.HTTP_200_OK,
                    )
                )
            else:
                perms = available_perm_status(request.user)

                return (
                    APIResponse.get_success_responses(
                        "You have the following permissions",
                        perms,
                        status_code=status.HTTP_200_OK,
                    )
                    if perms
                    else APIResponse.get_error_response(
                        "%s failed" % self.operation,
                        "You don't have any permissions",
                        status_code=status.HTTP_200_OK,
                    )
                )
        except get_user_model().DoesNotExist:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, user_id):
        """
        assign user permissions
        """
        self.operation = "Assign user permission"
        permission = request.data.get("permission")

        if not permission:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "Missing permission field",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if has_permission(request.user, "assign_user_permission"):
                user = get_user_model().objects.get(id=user_id)
                grant_permission(user, permission)

                return APIResponse.get_success_responses(
                    "User assigned %s permission successfully" % permission,
                    {"permission_assigned": permission},
                    status_code=status.HTTP_201_CREATED,
                )
            else:
                return APIResponse.get_error_response(
                    "%s failed" % self.operation,
                    "You do not have permission to assign user permissions",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
        except get_user_model().DoesNotExist:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except RolePermissionScopeException:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "User missing required role(s) for %s permission" % permission,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, user_id):
        """
        revoke user permissions
        """
        self.operation = "Revoke user permission"
        permission = request.data.get("permission")

        if not permission:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "Missing permission field",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        try:
            if has_permission(request.user, "revoke_user_permissions"):
                user = get_user_model().objects.get(id=user_id)
                revoke_permission(user, permission)

                return APIResponse.get_success_responses(
                    "user permission revoked successfully",
                    {"permission_revoked": permission},
                    status_code=status.HTTP_200_OK,
                )
            else:
                return APIResponse.get_error_response(
                    "%s failed" % self.operation,
                    "You do not have permission to revoke user permissions",
                    status_code=status.HTTP_403_FORBIDDEN,
                )
        except get_user_model().DoesNotExist:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "User with id %s does not exist" % user_id,
                status_code=status.HTTP_404_NOT_FOUND,
            )
        except RolePermissionScopeException:
            return APIResponse.get_error_response(
                "%s failed" % self.operation,
                "User missing required role(s) for %s permission" % permission,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
