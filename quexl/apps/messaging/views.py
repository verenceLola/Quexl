from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    DMMessagesSerializer,
    GroupMessagesSerializer,
    GroupSerializer,
)
from quexl.apps.messaging.models import Thread
from django.db.models import Q


class ListDMMessagesAPIView(ListAPIView):
    serializer_class = DMMessagesSerializer
    operation = "view dm messages"
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        return all messages where current user is participant
        """
        user = self.request.user
        return Thread.objects.filter(
            Q(participants=user) & Q(last_message__isnull=False) & Q(type="dm")
        )


class ListCreateGroupAPIiew(ListCreateAPIView):
    """
    create chat group
    """

    serializer_class = GroupSerializer
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

    def get(self, request, **kwargs):
        """
        override get method
        """
        self.operation = "View chat groups"
        return super(ListCreateAPIView, self).list(request, **kwargs)

    def create(self, request, **kwargs):
        """
        override post method
        """
        self.operation = "Create chat group"
        return super(ListCreateAPIView, self).create(request, **kwargs)


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
