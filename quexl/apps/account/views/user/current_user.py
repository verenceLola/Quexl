from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from quexl.apps.account.models import User
from quexl.apps.account.renderers import UserJSONRenderer
from quexl.apps.account.serializers import MeSerializer


class CurrentUserRetriveAPIView(RetrieveAPIView):
    """
    return the current user info
    """

    renderer_classes = (UserJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    serializer_class = MeSerializer

    def get_object(self):
        """
        retrive current user info
        """
        email = self.request.user.email

        return User.objects.get(email=email)
