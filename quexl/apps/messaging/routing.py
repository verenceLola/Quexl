from django.urls import path
from django.urls import re_path

from quexl.apps.messaging.views import ListCreateGroupAPIiew
from quexl.apps.messaging.views import ListDMMessagesAPIView
from quexl.apps.messaging.views import ListGroupMessages

from . import consumers

app_name = "messaging"

websocket_urlpatterns = [
    re_path(r"chat/dm/$", consumers.DMChatConsumer),  # dm messaging route
    re_path(
        r"chat/group/$", consumers.GroupChatConsumer
    ),  # group messaging route
    re_path(
        r"chat/broadcast/$", consumers.BroadcastChatConsumer
    ),  # broadcast messaging route
]

urlpatterns = [
    path(
        "dm/messages", ListDMMessagesAPIView.as_view(), name="user-dm-messages"
    ),
    path("group/", ListCreateGroupAPIiew.as_view(), name="user-groups"),
    path(
        "group/messages",
        ListGroupMessages.as_view(),
        name="user-group-messages",
    ),
]
