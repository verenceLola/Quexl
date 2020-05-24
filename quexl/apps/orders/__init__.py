"""register the signal handler for adding a history after adding a datafile"""

from django.apps import AppConfig


class OrdersAppConfig(AppConfig):
    """define the app config"""

    label = "orders"
    name = "quexl.apps.orders"
    verbose_name = "Orders"

    def ready(self) -> None:
        """
        register signal handlers when app is ready
        """
        from quexl.apps.orders.signals import data_file_history  # noqa


default_app_config = "quexl.apps.orders.OrdersAppConfig"
