from django.urls import resolve, reverse

import quexl.apps.account.views as views


def test_forgot_password_url_resolves():
    """
    test forgot password url resolves
    """
    url = reverse("authentication:forgot_password")
    assert resolve(url).func.view_class == views.ForgotPasswordView


def test_reset_password_url_resolves():
    """
    test reset pssword url resolves
    """
    url = reverse("authentication:reset_password", args=["reset token"])
    assert resolve(url).func.view_class == views.ResetPasswordView
