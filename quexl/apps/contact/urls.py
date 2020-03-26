"""urls for the orders app"""
from django.urls import path

# local imports
from quexl.apps.contact.views import ContactDetail
from quexl.apps.contact.views import ContactList

app_name = "contact"

urlpatterns = [
    path("contact/", ContactList.as_view(), name="contacts"),
    path("contact/<str:pk>", ContactDetail.as_view(), name="contact"),
]
