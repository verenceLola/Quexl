"""
services views
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from quexl.apps.services.models import (
    Service,
    Category,
    Order,
    Request,
    Payment,
)
from quexl.apps.services.permissions import (
    IsSellerOrReadOnly,
    IsSellerOrBuyer,
    IsBuyer,
)
from quexl.apps.services.serializers import (
    ServicesSerializer,
    CategorySerializer,
    OrdersSerializer,
    ServiceRequestSerializer,
    PaymentSerializer,
)
from rest_framework.permissions import IsAuthenticated
from quexl.apps.services.renderers import ServicesRenderer
from rest_framework import response, status


class APIViewWrapper(RetrieveUpdateDestroyAPIView):
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

    def get_queryset(self):
        """
        return given service_id instance
        """
        pk = self.kwargs.get(self.lookup_url_kwarg)
        return Service.objects.filter(id=pk)


class ServicesListCreateAPIView(ListCreateAPIView):
    """
    services view for listing and creating services
    """

    name = "service"
    pluralized_name = "services"
    permission_classes = (IsSellerOrReadOnly, IsAuthenticated)
    queryset = Service.objects.all()
    renderer_classes = (ServicesRenderer,)
    serializer_class = ServicesSerializer


class ServicesAPIView(APIViewWrapper, RetrieveUpdateDestroyAPIView):
    """
    service view for updating and deleting a service
    """

    permission_classes = (IsSellerOrReadOnly, IsAuthenticated)
    serializer_class = ServicesSerializer
    renderer_classes = (ServicesRenderer,)
    name = "service"
    pluralized_name = "services"
    lookup_url_kwarg = "service_id"


class CategoryListCreateAPIView(ListCreateAPIView):
    """
    categories view for listing and creating categories
    """

    name = "category"
    pluralized_name = "categories"
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.filter(level=0)  # get root nodes
    serializer_class = CategorySerializer
    renderer_classes = (ServicesRenderer,)


class CategoryUpdateDestroyAPIView(
    APIViewWrapper, RetrieveUpdateDestroyAPIView
):
    """
    categories view for updating and deleting categories
    """

    name = "category"
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    renderer_classes = (ServicesRenderer,)
    lookup_url_kwarg = "category_id"


class OrdersAPIView(ListCreateAPIView):
    """
    orders view
    """

    name = "order"
    pluralized_name = "orders"
    permission_classes = (IsSellerOrReadOnly, IsAuthenticated)
    serializer_class = OrdersSerializer
    renderer_classes = (ServicesRenderer,)
    lookup_url_kwarg = "service_id"

    def get_queryset(self):
        """
        return orders for specified service
        """
        service_id = self.kwargs.get(self.lookup_url_kwarg)
        return Order.objects.filter(service_id=service_id)


class OrdersRetriveUpdateDestroyAPIView(
    APIViewWrapper, RetrieveUpdateDestroyAPIView
):
    """
    manage service orders
    """

    name = "order"
    pluralized_name = "orders"
    permission_classes = (IsBuyer, IsAuthenticated)
    renderer_classes = (ServicesRenderer,)
    serializer_class = OrdersSerializer
    lookup_url_kwarg = "order_id"

    def get_queryset(self):
        """
        return order of given service
        """
        order_id = self.kwargs.get(self.lookup_url_kwarg)
        return Order.objects.filter(
            id=order_id
        )  # ignore service_id since order_id is unique


class ServiceRequestAPIView(ModelViewSet):
    """
    request service view
    """

    permission_classes = (IsSellerOrReadOnly, IsAuthenticated)
    queryset = Request.objects.all()
    serializer_class = ServiceRequestSerializer


class OrderPaymentsAPIView(ModelViewSet):
    """
    order payments view
    """

    permission_classes = (IsSellerOrBuyer, IsAuthenticated)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
