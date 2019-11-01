"""
urls for the services django app
"""
from quexl.apps.services.views import (
    ServicesAPIView,
    CategoryListCreateAPIView,
    CategoryUpdateDestroyAPIView,
    OrdersAPIView,
    ServicesViewSet,
    ServiceRequestAPIView,
    OrderPaymentsAPIView,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = "services"

seller_router = DefaultRouter()
seller_router.register(r"sell/payments", OrderPaymentsAPIView)
urlpatterns = [
    path("", include(seller_router.urls)),
    path("sell/services", ServicesViewSet.as_view(), name="user services"),
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
        OrdersAPIView.as_view({"get": "list"}),
        name="service orders",
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
