"""
signal to update service status upon successful creation of parameter template
"""
from typing import Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from quexl.apps.services.models import ParameterTemplate
from quexl.apps.services.models import Service


@receiver(post_save, sender=ParameterTemplate)
def update_service_status(sender: Type[ParameterTemplate], **kwargs) -> None:
    """
    update service status to success on successful creation of parameter
    template otherwise exceptions
    """
    parameter_template = kwargs["instance"]
    service_instance = Service.objects.get(pk=parameter_template.service.id)
    if kwargs["created"]:
        service_instance.service_status = "30"
    else:
        service_instance.service_status = "20"
    service_instance.save()
