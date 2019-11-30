from django.urls import path
from quexl.apps.profiles.views import ProfileGenericAPIView

app_name = "profiles"

urlpatterns = [
    path(
        "profile/<str:username>",
        ProfileGenericAPIView.as_view(),
        name="user_profiles",
    )
]
