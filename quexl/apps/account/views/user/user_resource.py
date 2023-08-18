from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from quexl.apps.account.models import User
from quexl.apps.account.serializers import UserSerializer


class UserResourceAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request: Request, user_id: str, *args, **kwargs) -> Response:
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        self.operation = "View user details"

        try:
            user = User.get_user_by_id(user_id=user_id)
            userdata = {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            }

            return Response(
                {
                    "message": "User details fetched successfully",
                    "details": userdata,
                },
                status=status.HTTP_200_OK,
            )

        except (KeyError, User.DoesNotExist, AttributeError):
            return Response(
                {
                    "message": "Failed to fetch user details",
                    "error": "That user id %s does not exist." % user_id,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request: Request, *args, **kwargs) -> Response:
        new_data = request.data
        self.operation = "Update user details"  # set operation name
        serializer = self.serializer_class(
            request.user, data=new_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        updated_fields = dict()

        for k, v in new_data.items():
            updated_fields.update({k: v})

        return Response(
            {
                "message": "User details successfully updated",
                "updated-fields": updated_fields,
                "new-record": new_data,
            },
            status=status.HTTP_200_OK,
        )
