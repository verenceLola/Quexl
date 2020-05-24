"""register the signal handler for updating status upon parameter templatte creation"""

from django.apps import AppConfig


class ServicesAppConfig(AppConfig):
    """define the app config"""

    label = "services"
    name = "quexl.apps.services"
    verbose_name = "Services"

    def ready(self) -> None:
        """
        register signal handlers when app is ready
        """
        from quexl.apps.services.signals import service_status  # noqa


default_app_config = "quexl.apps.services.ServicesAppConfig"
