from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from quexl.apps.messaging.models import Thread

from ..renderers import MessagesRenderer
from ..serializers import DMMessagesSerializer


class ListDMMessagesAPIView(ListAPIView):
    serializer_class = DMMessagesSerializer
    operation = "view dm messages"
    permission_classes = (IsAuthenticated,)
    pluralized_name = "messages"
    renderer_classes = (MessagesRenderer,)

    def get_queryset(self):
        """
        return all messages where current user is participant
        """
        user = self.request.user
        return Thread.objects.filter(
            Q(participants=user) & Q(last_message__isnull=False) & Q(type="dm")
        )
