from rolepermissions.roles import AbstractUserRole


class SiteAdminRole(AbstractUserRole):
    available_permissions = {
        "assign_user_roles": True,
        "remove_user_roles": True,
        "view_user_roles": True,
        "view_user_permissions": True,
        "revoke_user_permissions": True,
    }

    @classmethod
    def get_description(cls):
        """
        return roles description
        """

        return "Roles for Site Admin"

    @classmethod
    def get_name(cls):
        return "site_admin"


class DeveloperRole(AbstractUserRole):
    available_permissions = {
        "view_user_roles": True,
        "view_user_permissions": True,
    }

    @classmethod
    def get_description(cls):
        """
        return description of role
        """

        return "Roles for application developers"

    @classmethod
    def get_name(cls):
        return "developer"


class RegularUserRole(AbstractUserRole):
    available_permissions = {}

    @classmethod
    def get_description(cls):
        """
        return description of role
        """

        return "Roles for regular/ default user role"

    @classmethod
    def get_name(cls):
        return "regular_user"
