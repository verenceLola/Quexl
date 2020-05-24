from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

import quexl.apps.profiles.renderers as renderers
from quexl.apps.profiles.models import Profile
from quexl.apps.profiles.permissions import IsOwnerOrReadOnly
from quexl.apps.profiles.serializers import ProfileSerializer


class ProfileGenericAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ProfileSerializer
    lookup_url_kwarg = "id"
    renderer_classes = (renderers.ProfileRenderer,)
    lookup_field = "user__id"
    name = "profiles"
    queryset = Profile.objects.all()

    def update(self, request: Request, **kwargs) -> Response:
        """
        override updating user profile
        """
        self.operation = "Update user profile"

        return super(RetrieveUpdateAPIView, self).update(request, **kwargs)

    def get(self, request: Request, **kwargs) -> Response:
        """
        view user profile
        """
        self.operation = "View user profile"

        return super(RetrieveUpdateAPIView, self).retrieve(request, **kwargs)
