"""urls for the orders app"""
from django.urls import path

# local imports
from quexl.apps.orders.views import DataFileDetail
from quexl.apps.orders.views import DataFileList
from quexl.apps.orders.views import DownloadOrder
from quexl.apps.orders.views import HistoryDetail
from quexl.apps.orders.views import HistoryList
from quexl.apps.orders.views import OrderDetail
from quexl.apps.orders.views import OrderList
from quexl.apps.orders.views import ParameterDetail
from quexl.apps.orders.views import ParameterList
from quexl.apps.orders.views import RefreshOrder

app_name = "order"

urlpatterns = [
    path("data-file/", DataFileList.as_view(), name="data_files"),
    path("data-file/<str:pk>", DataFileDetail.as_view(), name="data_file"),
    path("buy/services/requests", OrderList.as_view(), name="orders"),
    path(
        "buy/services/requests/<str:pk>", OrderDetail.as_view(), name="order"
    ),
    path("parameter", ParameterList.as_view(), name="parameters",),
    path("parameter/<str:pk>", ParameterDetail.as_view(), name="parameter",),
    path("order/histories", HistoryList.as_view(), name="histories",),
    path("order/histories/<str:pk>", HistoryDetail.as_view(), name="history",),
    path(
        "order/refresh/<str:pk>", RefreshOrder.as_view(), name="refresh order",
    ),
    path(
        "order/download/<str:pk>",
        DownloadOrder.as_view(),
        name="download order",
    ),
]
