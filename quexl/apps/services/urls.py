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
    OrderPaymentsAPIView,
    OrdersRetriveUpdateDestroyAPIView,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = "services"

seller_router = DefaultRouter()
seller_router.register(r"sell/payments", OrderPaymentsAPIView)
urlpatterns = [
    path("", include(seller_router.urls)),
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
        "buy/services/request",
        ServiceRequestAPIView.as_view({"get": "list"}),
        name="request service",
    ),
    path(
        "sell/payments",
        OrderPaymentsAPIView.as_view({"get": "list"}),
        name="order payments",
    ),
]
