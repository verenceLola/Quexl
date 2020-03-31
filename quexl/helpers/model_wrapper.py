# common RetrieveUpdateDestroyAPIViewWrapper for models
from rest_framework import response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView


class RetrieveUpdateDestroyAPIViewWrapper(RetrieveUpdateDestroyAPIView):
    """
    prevent updating using PUT, define delete()
    """

    def put(self, request, **kwargs):
        """
        update object
        """
        return response.Response(
            {"message": "To update %s, use PATCH method" % self.name},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def delete(self, request, **kwargs):
        """
        delete category with all of its sub-categories
        """
        obj = self.get_object()
        obj.delete()
        return response.Response({}, status=status.HTTP_200_OK)
