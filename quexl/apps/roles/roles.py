from rolepermissions.roles import AbstractUserRole


class SiteAdmin(AbstractUserRole):
    """
    site admin role
    """

    available_permissions = {
        "assign_user_roles": True,
        "remove_user_roles": True,
        "view_user_roles": True,
        "view_user_permissions": True,
        "revoke_user_permissions": True,
        "edit_order_status": True,
    }

    @classmethod
    def get_description(self):
        """
        return roles description
        """
        return "Roles for Site Admin"


class Developer(AbstractUserRole):
    """"
    developer role
    """

    available_permissions = {
        "view_user_roles": True,
        "view_user_permissions": True,
        "edit_order_status": False,
    }

    @classmethod
    def get_description(self):
        """
        return description of role
        """
        return "Roles for application developers"


class RegularUser(AbstractUserRole):
    """
    regular user role
    """

    available_permissions = {}

    @classmethod
    def get_description(self):
        """
        return description of role
        """
        return "Roles for regular/ default user role"
