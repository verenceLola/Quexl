from django.urls import resolve
from django.urls import reverse

import quexl.apps.account.views as views


def test_register_url_resolves():
    """
    test the registrtion url resolves
    """
    url = reverse("authentication:user_signup")
    assert resolve(url).func.view_class == views.SignUpAPIView
