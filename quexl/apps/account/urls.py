from django.urls import path

import quexl.apps.account.views as views

app_name = "authentication"

urlpatterns = [
    path("auth/register", views.SignUpAPIView.as_view(), name="user_signup"),
    path("auth/login", views.LoginAPIView.as_view(), name="user_login"),
    path("auth/me", views.CurrentUserRetriveAPIView.as_view(), name="me"),
    path(
        "auth/<str:token>",
        views.UserActivationAPIView.as_view(),
        name="activate_user",
    ),
    path(
        "users/forgot_password",
        views.ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    path(
        "auth/reset_password/<str:token>",
        views.ResetPasswordView.as_view(),
        name="reset_password",
    ),
    path(
        "social-auth/login", views.SocialAuthView.as_view(), name="social_auth"
    ),
    path(
        "user/<str:user_id>", views.UserResourceAPIView.as_view(), name="user"
    ),
]
