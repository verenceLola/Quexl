"""
services views
"""
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
    IsBuyerOrReadOnly,
    IsBuyerOrSeller,
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
from django.db.models import Q


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


class ServicesAPIView(RetrieveUpdateDestroyAPIViewWrapper):
    """
    service view for updating and deleting a service
    """

    permission_classes = (IsSellerOrReadOnly, IsAuthenticated)
    serializer_class = ServicesSerializer
    renderer_classes = (ServicesRenderer,)
    name = "service"
    pluralized_name = "services"
    lookup_url_kwarg = "service_id"

    def get_queryset(self):
        """
        return given pk instance
        """
        pk = self.kwargs.get(self.lookup_url_kwarg)
        return Service.objects.filter(id=pk)


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


class CategoryUpdateDestroyAPIView(RetrieveUpdateDestroyAPIViewWrapper):
    """
    categories view for updating and deleting categories
    """

    name = "category"
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer
    renderer_classes = (ServicesRenderer,)
    lookup_url_kwarg = "category_id"

    def get_queryset(self):
        """
        return given pk instance
        """
        pk = self.kwargs.get(self.lookup_url_kwarg)
        return Category.objects.filter(id=pk)


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
        user = self.request.user
        return Order.objects.filter(
            Q(seller=user) | Q(buyer=user), service_id=service_id
        )


class OrdersRetriveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIViewWrapper):
    """
    manage service orders
    """

    name = "order"
    pluralized_name = "orders"
    permission_classes = (IsBuyerOrSeller, IsAuthenticated)
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


class ServiceRequestAPIView(ListCreateAPIView):
    """
    request service view for listing and creating service requests for buyers
    """

    name = "request"
    pluralized_name = "requests"
    permission_classes = (IsAuthenticated,)
    queryset = Request.objects.all()
    renderer_classes = (ServicesRenderer,)
    serializer_class = ServiceRequestSerializer


class ServiceRequestRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIViewWrapper
):
    """
    request service view for retrieving, updating and deleting a given request
    """

    name = "request"
    pluralized_name = "requests"
    permission_classes = (IsBuyerOrReadOnly, IsAuthenticated)
    renderer_classes = (ServicesRenderer,)
    serializer_class = ServiceRequestSerializer
    lookup_url_kwarg = "request_id"

    def get_queryset(self):
        """
        return given pk instance
        """
        pk = self.kwargs.get(self.lookup_url_kwarg)
        return Request.objects.filter(id=pk)


class OrderPaymentsAPIView(ListCreateAPIView):
    """
    order payments view
    """

    permission_classes = (IsBuyerOrReadOnly, IsAuthenticated)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
