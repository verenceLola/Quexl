from django.urls import resolve
from django.urls import reverse

from quexl.apps.messaging.views import ListCreateGroupAPIiew
from quexl.apps.messaging.views import ListDMMessagesAPIView


def test_dm_messages_resolves():
    """
    test fetch direct messages url resolves correctly
    """
    url = reverse("messaging:user-dm-messages")
    assert resolve(url).func.view_class == ListDMMessagesAPIView


def test_group_messages_resolves():
    """
    test fetch group messages url resolves
    """
    url = reverse("messaging:user-groups")
    assert resolve(url).func.view_class == ListCreateGroupAPIiew
