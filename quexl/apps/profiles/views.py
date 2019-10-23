from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from quexl.apps.profiles.permissions import IsOwnerOrReadOnly
from quexl.apps.profiles.serializers import ProfileSerializer
from quexl.apps.profiles.models import Profile
from quexl.apps.profiles.renderers import ProfileRenderer


class ProfileGenericAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ProfileSerializer
    lookup_url_kwarg = "profile_id"
    renderer_classes = (ProfileRenderer,)
    name = "profiles"

    def get_queryset(self):
        """
        return custom queryset
        """
        profile_id = self.kwargs.get(self.lookup_url_kwarg)
        return Profile.objects.filter(pk=profile_id)

    def update(self, request, **kwargs):
        """
        override updating user profile
        """
        self.operation = "Update user profile"
        return super(RetrieveUpdateAPIView, self).update(request, **kwargs)

    def get(self, request, **kwargs):
        """
        view user profile
        """
        self.operation = "View user profile"
        return super(RetrieveUpdateAPIView, self).retrieve(request, **kwargs)
