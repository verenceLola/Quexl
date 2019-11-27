from django.urls import resolve
from django.urls import reverse

import quexl.apps.account.views as views


def test_activate_user_url_resolves():
    """
    test activate user url resolves"""
    url = reverse("authentication:activate_user", args=["activation token"])
    assert resolve(url).func.view_class == views.UserActivationAPIView


def test_user_resource_url_resolves():
    """
    test user resource url resolves
    """
    url = reverse("authentication:user-details", args=[1])
    assert resolve(url).func.view_class == views.UserResourceAPIView


def test_current_user_url_resolves():
    """
    test getting current user url resolves
    """
    url = reverse("authentication:me")
    assert resolve(url).func.view_class == views.CurrentUserRetriveAPIView
