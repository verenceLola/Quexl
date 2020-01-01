from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from quexl.apps.messaging.models import Thread

from ..serializers import GroupMessagesSerializer


class ListGroupMessages(ListAPIView):
    """
    list all group messages of the current user
    """

    serializer_class = GroupMessagesSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        return all user groups
        """
        user = self.request.user
        return Thread.objects.filter(
            Q(participants=user)
            & Q(last_message__isnull=False)
            & Q(type="group")
        )
