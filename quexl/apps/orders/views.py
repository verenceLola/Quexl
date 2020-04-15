"""
orders views
"""
import asyncio
import os

import environ
import requests
from requests.auth import HTTPBasicAuth
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from quexl.apps.orders.models import DataFile
from quexl.apps.orders.models import History
from quexl.apps.orders.models import Order
from quexl.apps.orders.models import Parameter
from quexl.apps.orders.serializers import DataFileSerializer
from quexl.apps.orders.serializers import HistorySerializer
from quexl.apps.orders.serializers import OrderSerializer
from quexl.apps.orders.serializers import ParameterSerializer
from quexl.helpers.model_wrapper import RetrieveUpdateDestroyAPIViewWrapper
from quexl.helpers.permissions import IsBuyerOrReadOnly
from quexl.utils.renderers import DefaultRenderer


class ParameterList(ListCreateAPIView):
    """
    services view for listing and creating parameter s
    """

    name = "parameter"
    pluralized_name = "parameters"
    permission_classes = (IsAuthenticated,)
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    renderer_classes = (DefaultRenderer,)

    def create(self, request, **kwargs):
        """overide creating of parameter """
        self.operation = "Create parameter "
        return super(ListCreateAPIView, self).create(request, **kwargs)


class ParameterDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    service view for updating and deleting a parameter
    """

    permission_classes = (IsAuthenticated,)
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    renderer_classes = (DefaultRenderer,)
    name = "parameter"
    pluralized_name = "parameters"


class DataFileList(ListCreateAPIView):
    """view for listing and creating DataFile"""

    name = "data file"
    pluralized_name = "data files"
    permission_classes = (IsAuthenticated,)
    queryset = DataFile.objects.all()
    renderer_classes = (DefaultRenderer,)
    serializer_class = DataFileSerializer

    def create(self, request, **kwargs):
        """overide creating of data_file"""
        self.operation = "create data_file"
        return super(ListCreateAPIView, self).create(request, **kwargs)


class DataFileDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """view for retrieving, updating and destroying dataFiles"""

    name = "data file"
    pluralized_name = "data files"
    permission_class = (IsAuthenticated,)
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    renderer_classes = (DefaultRenderer,)

    def update(self, request, *args, **kwargs):
        """overide the update method"""
        self.operation = "data_file"
        return self.super(RetrieveUpdateDestroyAPIViewWrapper, self).update(
            request, *args, **kwargs
        )


class OrderList(ListCreateAPIView):
    """view for creating and listing orders"""

    name = "order"
    pluralized_name = "orders"
    permission_classes = (IsAuthenticated, IsBuyerOrReadOnly)
    renderer_classes = (DefaultRenderer,)
    serializer_class = OrderSerializer

    def create(self, request, **kwargs):
        """overide creating of order"""
        self.operation = "Create order"
        return super(ListCreateAPIView, self).create(request, **kwargs)

    def get_queryset(self):
        service = self.request.query_params.get("service")
        if service:
            orders = (
                Order.objects.filter(buyer=self.request.user.id)
                .filter(service=service)
                .order_by("updated_at")
            )
        else:
            orders = Order.objects.filter(buyer=self.request.user.id).order_by(
                "-updated_at"
            )
        return orders


class OrderDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """view for retrieving, updating and destroying an order"""

    name = "order"
    pluralized_name = "orders"
    permission_classes = (IsAuthenticated, IsBuyerOrReadOnly)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    renderer_classes = (DefaultRenderer,)

    def update(self, request, *args, **kwargs):
        self.operation = "update order"
        return super(RetrieveUpdateDestroyAPIViewWrapper, self).update(
            request, *args, **kwargs
        )


class HistoryList(ListAPIView):
    """view for listing Histories"""

    pluralized_name = "histories"
    permission_classes = (IsAuthenticated,)
    queryset = History.objects.all()
    renderer_classes = (DefaultRenderer,)
    serializer_class = HistorySerializer


class HistoryDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """view for retrieving, updating and destroying a history"""

    name = "history"
    pluralized_name = "histories"
    permission_classes = (IsAuthenticated,)
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    renderer_classes = (DefaultRenderer,)

    def update(self, request, *args, **kwargs):
        self.operation = "update history"
        return super(RetrieveUpdateDestroyAPIViewWrapper, self).update(
            request, *args, **kwargs
        )


async def check_status(queryset):  # pragma: no cover
    api_key = environ.Env().read_env()
    api_key = os.environ.get("EXTERNAL_API_KEY")
    uri = "https://sandbox.zamzar.com/v1/jobs/{}".format(queryset.job_id)
    response = requests.get(uri, auth=HTTPBasicAuth(api_key, ""))
    try:
        if response.json()["status"] == "successful":
            data = {"status": "COMPLETED"}
            serializer = OrderSerializer(queryset, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return response
    except BaseException:
        raise NotFound("Resource not found")


class RefreshOrder(RetrieveAPIView):
    """view for refreshing an order"""

    name = "order query"
    permission_classes = (IsAuthenticated, IsBuyerOrReadOnly)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    renderer_classes = (DefaultRenderer,)

    def retrieve(self, request, *args, **kwargs):  # pragma: no cover
        self.operation = "update order"
        queryset = Order.objects.get(pk=kwargs.get("pk"))

        async def main():
            await check_status(queryset)

        asyncio.run(main())
        return super(RetrieveAPIView, self).retrieve(request, *args, **kwargs)


class DownloadOrder(RetrieveAPIView):
    """view downloading an order"""

    name = "download order"
    permission_classes = (IsAuthenticated, IsBuyerOrReadOnly)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    renderer_classes = (DefaultRenderer,)

    def retrieve(self, request, *args, **kwargs):  # pragma: no cover
        self.operation = "download order"
        order_query = Order.objects.get(pk=kwargs.get("pk"))

        async def download_order(res):
            file_name = res.json()["target_files"][0]["name"]
            file_id = res.json()["target_files"][0]["id"]
            api_key = os.environ.get("EXTERNAL_API_KEY")
            endpoint = "https://sandbox.zamzar.com/v1/files/{}/content".format(
                file_id
            )
            response = requests.get(
                endpoint, stream=True, auth=HTTPBasicAuth(api_key, "")
            )
            file_path = "uploads/{}".format(file_name)
            try:
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            f.flush()
            except BaseException:
                raise NotFound("Resource not found")

        async def main():
            res = await check_status(order_query)
            await download_order(res)

        asyncio.run(main())
        return super(RetrieveAPIView, self).retrieve(request, *args, **kwargs)
