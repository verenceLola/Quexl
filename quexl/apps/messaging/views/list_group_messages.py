from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from quexl.apps.messaging.models import Thread
from quexl.utils.renderers import DefaultRenderer

from ..serializers import GroupMessagesSerializer


class ListGroupMessages(ListAPIView):
    """
    list all group messages of the current user
    """

    serializer_class = GroupMessagesSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (DefaultRenderer,)
    pluralized_name = "group messages"

    def get_queryset(self) -> QuerySet:
        """
        return all user groups
        """
        user = self.request.user
        return Thread.objects.filter(
            Q(participants=user)
            & Q(last_message__isnull=False)
            & Q(type="group")
        )
