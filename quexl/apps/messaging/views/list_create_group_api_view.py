from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

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

    def get_queryset(self) -> QuerySet:
        """
        return all user groups
        """
        user = self.request.user
        return Thread.objects.filter(Q(participants=user) & Q(type="group"))

    def get(self, request: Request, **kwargs) -> Response:
        """
        override get method
        """
        self.operation = "View chat groups"
        return super(ListCreateAPIView, self).list(request, **kwargs)

    def create(self, request: Request, **kwargs):
        """
        override post method
        """
        self.operation = "Create chat group"
        return super(ListCreateAPIView, self).create(request, **kwargs)
