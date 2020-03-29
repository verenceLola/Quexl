"""
test profiles urls
"""
from django.urls import resolve
from django.urls import reverse

from quexl.apps.profiles.views import ProfileGenericAPIView


def test_profile_url_resolves():
    """
    test the profile url resolves to expected view
    """
    url = reverse("profiles:user_profiles", args=["profile_id"])
    assert resolve(url).func.view_class == ProfileGenericAPIView
