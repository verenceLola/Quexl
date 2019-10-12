from django.urls import reverse, resolve
from quexl.apps.authentication.views import (
    RegistrationAPIView,
    LoginAPIView,
    ForgotPasswordView,
    UserActivationAPIView,
    ResetPasswordView,
    UserResourceAPIView,
)


def test_register_url_resolves():
    """
    test the registrtion url resolves
    """
    url = reverse("authentication:user_signup")
    assert resolve(url).func.view_class == RegistrationAPIView


def test_login_url_resolves():
    """
    test the login url resolves
    """
    url = reverse("authentication:user_login")
    assert resolve(url).func.view_class == LoginAPIView


def test_forgot_password_url_resolves():
    """
    test forgot password url resolves
    """
    url = reverse("authentication:forgot_password")
    assert resolve(url).func.view_class == ForgotPasswordView


def test_activate_user_url_resolves():
    """
    test activate user url resolves"""
    url = reverse("authentication:activate_user", args=["activation token"])
    assert resolve(url).func.view_class == UserActivationAPIView


def reset_password_url_resolves():
    """
    test reset pssword url resolves
    """
    url = reverse("authentication:reset_password", args=["reset token"])
    assert resolve(url).func.view_class == ResetPasswordView


def test_user_resource_url_resolves():
    """
    test user resource url resolves
    """
    url = reverse("authentication:user", args=[1])
    assert resolve(url).func.view_class == UserResourceAPIView
