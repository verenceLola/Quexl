"""urls for the orders app"""
from django.urls import path
from django.urls import re_path

# local imports
from quexl.apps.orders import views

app_name = "order"

urlpatterns = [
    path("data-file/", views.DataFileList.as_view(), name="data_files"),
    path(
        "data-file/<str:pk>", views.DataFileDetail.as_view(), name="data_file"
    ),
    path("buy/services/requests", views.OrderList.as_view(), name="orders"),
    path(
        "buy/services/requests/<str:pk>",
        views.OrderDetail.as_view(),
        name="order",
    ),
    path("parameter", views.ParameterList.as_view(), name="parameters",),
    path(
        "parameter/<str:pk>",
        views.ParameterDetail.as_view(),
        name="parameter",
    ),
    path("order/histories", views.HistoryList.as_view(), name="histories",),
    path(
        "order/histories/<str:pk>",
        views.HistoryDetail.as_view(),
        name="history",
    ),
    path(
        "order/refresh/<str:pk>",
        views.RefreshOrder.as_view(),
        name="refresh order",
    ),
    path(
        "order/download/<str:pk>",
        views.DownloadOrder.as_view(),
        name="download order",
    ),
    re_path(r"^paypal/$", views.MakePayment.as_view(), name="paypal"),
]
