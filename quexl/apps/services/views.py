"""
services views
"""
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from quexl.apps.orders.models import Order
from quexl.apps.orders.serializers import OrderSerializer
from quexl.apps.services.models import Category
from quexl.apps.services.models import DataFormat
from quexl.apps.services.models import Gallery
from quexl.apps.services.models import OutputFile
from quexl.apps.services.models import ParameterOption
from quexl.apps.services.models import ParameterTemplate
from quexl.apps.services.models import Service
from quexl.apps.services.serializers import CategorySerializer
from quexl.apps.services.serializers import DataFormatSerializer
from quexl.apps.services.serializers import GallerySerializer
from quexl.apps.services.serializers import OutputFileSerializer
from quexl.apps.services.serializers import ParameterOptionSerializer
from quexl.apps.services.serializers import ParameterTemplateSerializer
from quexl.apps.services.serializers import ServicesSerializer
from quexl.helpers.model_wrapper import RetrieveUpdateDestroyAPIViewWrapper
from quexl.helpers.permissions import IsSellerOrReadOnly
from quexl.utils.renderers import DefaultRenderer


class CategoryList(ListCreateAPIView):
    """
    categories view for listing and creating categories
    """

    name = "category"
    pluralized_name = "categories"
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.filter(level=0)  # get root nodes
    serializer_class = CategorySerializer
    renderer_classes = (DefaultRenderer,)

    def create(self, request, **kwargs):
        """overide creating of category"""
        self.operation = "create category"
        return super(ListCreateAPIView, self).create(request, **kwargs)


class CategoryDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    categories view for updating and deleting categories
    """

    pluralized_name = "categories"
    name = "category"
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    renderer_classes = (DefaultRenderer,)

    def update(self, request, *args, **kwargs):
        self.operation = "category"
        return super(RetrieveUpdateDestroyAPIViewWrapper, self).update(
            request, *args, **kwargs
        )


class ServicesList(ListCreateAPIView):
    """
    services view for listing and creating services
    """

    name = "service"
    pluralized_name = "services"
    permission_classes = (IsSellerOrReadOnly, IsAuthenticated)
    queryset = Service.objects.all()
    renderer_classes = (DefaultRenderer,)
    serializer_class = ServicesSerializer

    def create(self, request, **kwargs):
        """overide creating of service"""
        self.operation = "Create service"
        return super(ListCreateAPIView, self).create(request, **kwargs)


class ServicesDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    service view for updating and deleting a service
    """

    permission_classes = (IsSellerOrReadOnly, IsAuthenticated)
    queryset = Service.objects.all()
    serializer_class = ServicesSerializer
    renderer_classes = (DefaultRenderer,)
    name = "service"
    pluralized_name = "services"

    def update(self, request, *args, **kwargs):
        self.operation = "service"
        return super(RetrieveUpdateDestroyAPIViewWrapper, self).update(
            request, *args, **kwargs
        )


class ServiceOrdersList(ListAPIView):
    """view orders for a specific service"""

    name = "seller order"
    pluralized_name = "seller orders"
    permission_classes = (IsAuthenticated, IsSellerOrReadOnly)
    renderer_classes = (DefaultRenderer,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        service = self.request.query_params.get("service")
        orders = Order.objects.filter(service=service).filter(
            service__seller=self.request.user
        )
        return orders


class DataFormatList(ListCreateAPIView):
    """
    services view for listing and creating data formats
    """

    name = "data_format"
    pluralized_name = "data_formats"
    permission_classes = (IsAuthenticated,)
    queryset = DataFormat.objects.all()
    renderer_classes = (DefaultRenderer,)
    serializer_class = DataFormatSerializer


class DataFormatDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    service view for updating and deleting a data format
    """

    permission_classes = (IsAuthenticated,)
    queryset = DataFormat.objects.all()
    serializer_class = DataFormatSerializer
    renderer_classes = (DefaultRenderer,)
    name = "data format"
    pluralized_name = "data formats"


class ParameterTemplateList(ListCreateAPIView):
    """
    services view for listing and creating parameter templates
    """

    name = "parameter_template"
    pluralized_name = "parameter_templates"
    permission_classes = (IsAuthenticated,)
    queryset = ParameterTemplate.objects.all()
    renderer_classes = (DefaultRenderer,)
    serializer_class = ParameterTemplateSerializer

    def create(self, request, **kwargs):
        """overide creating of parameter template"""
        self.operation = "Create parameter template"
        return super(ListCreateAPIView, self).create(request, **kwargs)


class ParameterTemplateDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    service view for updating and deleting a parameter template
    """

    permission_classes = (IsAuthenticated,)
    queryset = ParameterTemplate.objects.all()
    serializer_class = ParameterTemplateSerializer
    renderer_classes = (DefaultRenderer,)
    name = "parameter template"
    pluralized_name = "parameter templates"


class ParameterOptionList(ListCreateAPIView):
    """
    services view for listing and creating parameter options
    """

    name = "parameter_option"
    pluralized_name = "parameter_options"
    permission_classes = (IsAuthenticated,)
    queryset = ParameterOption.objects.all()
    serializer_class = ParameterOptionSerializer
    renderer_classes = (DefaultRenderer,)

    def create(self, request, **kwargs):
        """overide creating of parameter option"""
        self.operation = "Create parameter option"
        return super(ListCreateAPIView, self).create(request, **kwargs)


class ParameterOptionDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    service view for updating and deleting a parameter option
    """

    permission_classes = (IsAuthenticated,)
    queryset = ParameterOption.objects.all()
    serializer_class = ParameterOptionSerializer
    renderer_classes = (DefaultRenderer,)
    name = "parameter option"
    pluralized_name = "parameter options"


class OutputFileList(ListCreateAPIView):
    """
    services view for listing and creating parameter options
    """

    name = "output_file"
    pluralized_name = "output_files"
    permission_classes = (IsAuthenticated,)
    queryset = OutputFile.objects.all()
    serializer_class = OutputFileSerializer
    renderer_classes = (DefaultRenderer,)

    def create(self, request, **kwargs):
        """overide creating of output file"""
        self.operation = "Create output file"
        return super(ListCreateAPIView, self).create(request, **kwargs)


class OutputFileDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    service view for updating and deleting an output file
    """

    permission_classes = (IsAuthenticated,)
    queryset = OutputFile.objects.all()
    serializer_class = OutputFileSerializer
    renderer_classes = (DefaultRenderer,)
    name = "output file"
    pluralized_name = "output files"


class GalleryList(ListCreateAPIView):
    """
    services view for listing and creating gallery
    """

    name = "gallery"
    pluralized_name = "galleries"
    permission_classes = (IsSellerOrReadOnly, IsAuthenticated)
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    renderer_classes = (DefaultRenderer,)

    def create(self, request, **kwargs):
        """overide creating of gallery"""
        self.operation = "Create gallery"
        return super(ListCreateAPIView, self).create(request, **kwargs)


class GalleryDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    service view for updating and deleting an gallery
    """

    permission_classes = (IsAuthenticated,)
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    renderer_classes = (DefaultRenderer,)
    name = "gallery"
    pluralized_name = "galleries"

    def update(self, request, *args, **kwargs):
        self.operation = "gallery"
        return super(RetrieveUpdateDestroyAPIViewWrapper, self).update(
            request, *args, **kwargs
        )
