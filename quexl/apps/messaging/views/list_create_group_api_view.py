from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from quexl.apps.messaging.models import Thread
from quexl.utils.renderers import DefaultRenderer

from ..serializers import GroupSerializer


class ListCreateGroupAPIiew(ListCreateAPIView):
    """
    create chat group
    """

    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (DefaultRenderer,)
    name = "group"
    pluralized_name = "groups"

    def get_queryset(self):
        """
        return all user groups
        """
        user = self.request.user
        return Thread.objects.filter(Q(participants=user) & Q(type="group"))

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
