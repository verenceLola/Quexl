"""
quexl URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("quexl.apps.account.urls")),
    path("", include("social_django.urls", namespace="social-auth")),  # noqa
    path("api/", include("quexl.apps.roles.urls")),
    path("api/users/", include("quexl.apps.profiles.urls")),
    path("api/", include("quexl.apps.services.urls")),
]
