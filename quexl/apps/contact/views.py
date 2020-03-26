from django.shortcuts import render
from .models import Contact
from .serializers import ContactSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import response
from rest_framework import status

from quexl.utils.renderers import DefaultRenderer

from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

class ContactList(ListCreateAPIView):
    """
    services view for listing and creating contact
    """
    name = "contact"
    pluralized_name = "contacts"
    # permission_classes = (IsAuthenticated,)
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    renderer_classes = (DefaultRenderer,)

    def create(self, request, **kwargs):
        """overide creating of contact """
        self.operation = "Create contact "
        return super(ListCreateAPIView, self).create(request, **kwargs)

class ContactDetail(RetrieveDestroyAPIView):
    """view for retrieving and destroying a contact"""
    name = "contact"
    pluralized_name = "contacts"
    permission_classes = (IsAuthenticated, )
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    renderer_classes = (DefaultRenderer,)

    def delete(self, request, **kwargs):
        """
        delete contact
        """
        obj = self.get_object()
        obj.delete()
        return response.Response({}, status=status.HTTP_200_OK)