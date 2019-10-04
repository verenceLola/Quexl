from django.urls import path

from .views import (
    RegistrationAPIView,
    LoginAPIView,
    UserActivationAPIView,
    UserResourceAPIView
)

urlpatterns = [
    path('users/register', RegistrationAPIView.as_view(),
         name='user_signup'),
    path('users/login', LoginAPIView.as_view(),
         name='user_login'),
    path('auth/<str:token>', UserActivationAPIView.as_view(),
         name='activate_user'),
    path('user/<str:user_id>', UserResourceAPIView.as_view(),
         name="user"),
]
