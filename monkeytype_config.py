import os
from contextlib import contextmanager
from typing import Iterator

from monkeytype.config import DefaultConfig


class QuexlConfig(DefaultConfig):
    """
    monkey type config for django code
    """

    @contextmanager
    def cli_context(self, command: str) -> Iterator[None]:
        import django

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quexl.settings")
        django.setup()
        yield


CONFIG = QuexlConfig()
