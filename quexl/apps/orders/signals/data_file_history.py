"""
signal to create history after uploading a datafile
"""
from typing import Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from quexl.apps.orders.models import DataFile
from quexl.apps.orders.models import History


@receiver(post_save, sender=DataFile)
def create_data_file_history(sender: Type[DataFile], **kwargs) -> None:
    """
    add a history when a datafile is added
    """
    data_file = kwargs["instance"]

    if kwargs["created"]:
        data = {
            "description": data_file.name + " upload",
            "history_owner": data_file.file_owner,
        }
        instance = History.objects.create(**data)
        instance.data_file.set([data_file])
