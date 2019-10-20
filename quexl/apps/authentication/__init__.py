"""register the signal handler for creating the new
    user profile upon successful registration"""

from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    """define the app config"""

    label = "authentication"
    name = "quexl.apps.authentication"
    verbose_name = "Authentication"

    def ready(self):
        """
        register signal handlers when app is ready
        """
        from quexl.apps.authentication.signals import roles  # noqa


default_app_config = "quexl.apps.authentication.AuthenticationAppConfig"
