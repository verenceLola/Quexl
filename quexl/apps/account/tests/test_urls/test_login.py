from django.urls import resolve
from django.urls import reverse

import quexl.apps.account.views as views


def test_login_url_resolves():
    """
    test the login url resolves
    """
    url = reverse("authentication:user_login")
    assert resolve(url).func.view_class == views.LoginAPIView
