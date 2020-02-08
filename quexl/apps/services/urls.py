"""
urls for the services django app
"""
from django.urls import path

from quexl.apps.services.views import CategoryDetail
from quexl.apps.services.views import CategoryList
from quexl.apps.services.views import DataFormatDetail
from quexl.apps.services.views import DataFormatList
from quexl.apps.services.views import GalleryDetail
from quexl.apps.services.views import GalleryList
from quexl.apps.services.views import OutputFileDetail
from quexl.apps.services.views import OutputFileList
from quexl.apps.services.views import ParameterOptionDetail
from quexl.apps.services.views import ParameterOptionList
from quexl.apps.services.views import ParameterTemplateDetail
from quexl.apps.services.views import ParameterTemplateList
from quexl.apps.services.views import ServiceOrdersList
from quexl.apps.services.views import ServicesDetail
from quexl.apps.services.views import ServicesList

app_name = "services"

urlpatterns = [
    path("categories/", CategoryList.as_view(), name="categories",),
    path("categories/<str:pk>", CategoryDetail.as_view(), name="category",),
    path("sell/services", ServicesList.as_view(), name="services",),
    path("sell/orders", ServiceOrdersList.as_view(), name="service orders",),
    path("sell/services/<str:pk>", ServicesDetail.as_view(), name="service",),
    path(
        "parameter-template",
        ParameterTemplateList.as_view(),
        name="parameter_templates",
    ),
    path(
        "parameter-template/<str:pk>",
        ParameterTemplateDetail.as_view(),
        name="parameter_template",
    ),
    path(
        "parameter-option",
        ParameterOptionList.as_view(),
        name="parameter_options",
    ),
    path(
        "parameter-option/<str:pk>",
        ParameterOptionDetail.as_view(),
        name="parameter_option",
    ),
    path("data-format", DataFormatList.as_view(), name="data_formats",),
    path(
        "data-format/<str:pk>", DataFormatDetail.as_view(), name="data_format",
    ),
    path("output-file", OutputFileList.as_view(), name="output_files",),
    path(
        "output-file/<str:pk>", OutputFileDetail.as_view(), name="output_file",
    ),
    path("gallery", GalleryList.as_view(), name="galleries",),
    path("gallery/<str:pk>", GalleryDetail.as_view(), name="gallery",),
]
