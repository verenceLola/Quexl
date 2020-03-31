"""
quexl URL Configuration
"""
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("quexl.apps.account.urls")),
    path("", include("social_django.urls", namespace="social-auth")),  # noqa
    path("api/", include("quexl.apps.roles.urls")),
    path("api/users/", include("quexl.apps.profiles.urls")),
    path("api/user/", include("quexl.apps.messaging.routing")),
    path("api/", include("quexl.apps.services.urls")),
    path("api/", include("quexl.apps.orders.urls")),
    path("api/", include("quexl.apps.contact.urls")),
    path("api/", include("quexl.apps.blog.urls")),
]
