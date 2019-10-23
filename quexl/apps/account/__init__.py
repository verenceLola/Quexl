"""register the signal handler for creating the new
    user profile upon successful registration"""

from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    """define the app config"""

    label = "account"
    name = "quexl.apps.account"
    verbose_name = "Account"

    def ready(self):
        """
        register signal handlers when app is ready
        """
        from quexl.apps.account.signals import roles  # noqa
        from quexl.apps.account.signals import profiles  # noqa


default_app_config = "quexl.apps.account.AuthenticationAppConfig"
