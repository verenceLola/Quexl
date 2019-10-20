from django.urls import path
from quexl.apps.roles.views import UserRoleAPIView, PermissionsAPIView


app_name = "roles"

urlpatterns = [
    path(
        "users/<str:user_id>/roles",
        UserRoleAPIView.as_view(),
        name="user roles",
    ),
    path(
        "users/<str:user_id>/permissions",
        PermissionsAPIView.as_view(),
        name="user permissions",
    ),
]
