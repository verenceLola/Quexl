from django.urls import path

from .views import (
    RegistrationAPIView,
    LoginAPIView,
    UserActivationAPIView,
    UserResourceAPIView,
    ForgotPasswordView,
    ResetPasswordView
)

urlpatterns = [
    path('users/register', RegistrationAPIView.as_view(),
         name='user_signup'),
    path('users/login', LoginAPIView.as_view(),
         name='user_login'),
    path('auth/<str:token>', UserActivationAPIView.as_view(),
         name='activate_user'),
    path('users/forgot_password', ForgotPasswordView.as_view(),
         name="forgot_password"),
    path('users/reset_password/<str:token>', ResetPasswordView.as_view(),
         name="reset_password"),
    path('user/<str:user_id>', UserResourceAPIView.as_view(),
         name="user"),
]
