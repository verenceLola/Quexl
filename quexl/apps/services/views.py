"""
services views
"""
from rest_framework import response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from quexl.apps.services.models import Category
from quexl.apps.services.models import DataFormat
from quexl.apps.services.models import Gallery
from quexl.apps.services.models import OutputFile
from quexl.apps.services.models import ParamerterOption
from quexl.apps.services.models import ParamerterTemplate
from quexl.apps.services.models import Service
from quexl.apps.services.permissions import IsSellerOrReadOnly
from quexl.apps.services.renderers import ServicesRenderer
from quexl.apps.services.serializers import CategorySerializer
from quexl.apps.services.serializers import DataFormatSerializer
from quexl.apps.services.serializers import GallerySerializer
from quexl.apps.services.serializers import OutputFileSerializer
from quexl.apps.services.serializers import ParameterOptionSerializer
from quexl.apps.services.serializers import ParameterTemplateSerializer
from quexl.apps.services.serializers import ServicesSerializer


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


class CategoryList(ListCreateAPIView):
    """
    categories view for listing and creating categories
    """

    name = "category"
    pluralized_name = "categories"
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.filter(level=0)  # get root nodes
    serializer_class = CategorySerializer
    renderer_classes = (ServicesRenderer,)

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
    renderer_classes = (ServicesRenderer,)

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
    renderer_classes = (ServicesRenderer,)
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
    renderer_classes = (ServicesRenderer,)
    name = "service"
    pluralized_name = "services"

    def update(self, request, *args, **kwargs):
        self.operation = "service"
        return super(RetrieveUpdateDestroyAPIViewWrapper, self).update(
            request, *args, **kwargs
        )


class DataFormatList(ListCreateAPIView):
    """
    services view for listing and creating data formats
    """

    name = "data_format"
    pluralized_name = "data_formats"
    permission_classes = (IsAuthenticated,)
    queryset = DataFormat.objects.all()
    renderer_classes = (ServicesRenderer,)
    serializer_class = DataFormatSerializer


class DataFormatDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    service view for updating and deleting a data format
    """

    permission_classes = (IsAuthenticated,)
    queryset = DataFormat.objects.all()
    serializer_class = DataFormatSerializer
    renderer_classes = (ServicesRenderer,)
    name = "data format"
    pluralized_name = "data formats"


class ParameterTemplateList(ListCreateAPIView):
    """
    services view for listing and creating parameter templates
    """

    name = "parameter_template"
    pluralized_name = "parameter_templates"
    permission_classes = (IsAuthenticated,)
    queryset = ParamerterTemplate.objects.all()
    renderer_classes = (ServicesRenderer,)
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
    queryset = ParamerterTemplate.objects.all()
    serializer_class = ParameterTemplateSerializer
    renderer_classes = (ServicesRenderer,)
    name = "parameter template"
    pluralized_name = "parameter templates"


class ParameterOptionList(ListCreateAPIView):
    """
    services view for listing and creating parameter options
    """

    name = "parameter_option"
    pluralized_name = "parameter_options"
    permission_classes = (IsAuthenticated,)
    queryset = ParamerterOption.objects.all()
    serializer_class = ParameterOptionSerializer
    renderer_classes = (ServicesRenderer,)

    def create(self, request, **kwargs):
        """overide creating of parameter option"""
        self.operation = "Create parameter option"
        return super(ListCreateAPIView, self).create(request, **kwargs)


class ParameterOptionDetail(RetrieveUpdateDestroyAPIViewWrapper):
    """
    service view for updating and deleting a parameter option
    """

    permission_classes = (IsAuthenticated,)
    queryset = ParamerterOption.objects.all()
    serializer_class = ParameterOptionSerializer
    renderer_classes = (ServicesRenderer,)
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
    renderer_classes = (ServicesRenderer,)

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
    renderer_classes = (ServicesRenderer,)
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
    renderer_classes = (ServicesRenderer,)

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
    renderer_classes = (ServicesRenderer,)
    name = "gallery"
    pluralized_name = "galleries"

    def update(self, request, *args, **kwargs):
        self.operation = "gallery"
        return super(RetrieveUpdateDestroyAPIViewWrapper, self).update(
            request, *args, **kwargs
        )
