from django.urls import resolve
from django.urls import reverse

from quexl.apps.roles.views import PermissionsAPIView
from quexl.apps.roles.views import UserRoleAPIView


def test_user_roles_url_resolves():
    """
    test user roles url resolves correctly
    """
    url = reverse("roles:user roles", args=["access_token"])
    assert resolve(url).func.view_class == UserRoleAPIView


def test_user_permissions_url_resolves():
    """
    test user permissions url resolves correctly
    """
    url = reverse("roles:user permissions", args=["access_token"])
    assert resolve(url).func.view_class == PermissionsAPIView
