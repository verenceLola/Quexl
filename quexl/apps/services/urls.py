"""
urls for the services django app
"""
from quexl.apps.services.views import (
    ServicesAPIView,
    CategoryListCreateAPIView,
    CategoryUpdateDestroyAPIView,
    OrdersAPIView,
    ServicesListCreateAPIView,
    ServiceRequestAPIView,
    ServiceRequestRetrieveUpdateDestroyAPIView,
    OrderPaymentsAPIView,
    OrdersRetriveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "services"

urlpatterns = [
    path(
        "sell/services",
        ServicesListCreateAPIView.as_view(),
        name="user services",
    ),
    path(
        "sell/services/<str:service_id>",
        ServicesAPIView.as_view(),
        name="update-delete service",
    ),
    path(
        "categories/",
        CategoryListCreateAPIView.as_view(),
        name="list create categories",
    ),
    path(
        "categories/<str:category_id>",
        CategoryUpdateDestroyAPIView.as_view(),
        name="update destroy categories",
    ),
    path(
        "sell/services/<str:service_id>/orders",
        OrdersAPIView.as_view(),
        name="list create service orders",
    ),
    path(
        "sell/services/<str:service_id>/orders/<str:order_id>",
        OrdersRetriveUpdateDestroyAPIView.as_view(),
        name="retrieve, update, delete service order",
    ),
    path(
        "buy/services/requests",
        ServiceRequestAPIView.as_view(),
        name="list create service request",
    ),
    path(
        "buy/services/requests/<str:request_id>",
        ServiceRequestRetrieveUpdateDestroyAPIView.as_view(),
        name="edit delete service request ",
    ),
    path(
        "orders/<str:order_id>/payment",
        OrderPaymentsAPIView.as_view(),
        name="order payment",
    ),
]
