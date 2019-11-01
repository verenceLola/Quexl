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
from quexl.apps.services.permissions import IsOwnerOrReadOnly, IsSellerOrBuyer
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


class ServicesAPIView(ModelViewSet):
    """
    services view
    """

    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer


class CategoryListCreateAPIView(ListCreateAPIView):
    """
    categories view for listing and creating categories
    """

    name = "category"
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.filter(level=0)  # get root nodes
    serializer_class = CategorySerializer
    renderer_classes = (ServicesRenderer,)


class CategoryUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
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
        return specific category
        """
        category_id = self.kwargs.get(self.lookup_url_kwarg)
        return Category.objects.filter(id=category_id)

    def put(self, request, **kwargs):
        """
        update category details
        """
        return response.Response(
            {"message": "To update category, use PATCH method"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def delete(self, request, category_id):
        """
        delete category with all of its sub-categories
        """
        category = self.get_object()
        category.delete()
        return response.Response({}, status=status.HTTP_200_OK)


class OrdersAPIView(ModelViewSet):
    """
    orders view
    """

    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    serializer_class = OrdersSerializer
    lookup_url_kwarg = "service_id"

    def get_queryset(self):
        """
        return orders for specified service
        """
        service_id = self.kwargs.get(self.lookup_url_kwarg)
        return Order.objects.filter(service_id=service_id)


class ServiceRequestAPIView(ModelViewSet):
    """
    request service view
    """

    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    queryset = Request.objects.all()
    serializer_class = ServiceRequestSerializer


class OrderPaymentsAPIView(ModelViewSet):
    """
    order payments view
    """

    permission_classes = (IsSellerOrBuyer, IsAuthenticated)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
