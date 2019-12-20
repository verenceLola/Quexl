"""
signal to add regular user role to every new user
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from rolepermissions.roles import assign_role

from quexl.apps.account.models import User


@receiver(post_save, sender=User)
def add_regular_user_role(sender, **kwargs):

    if kwargs["created"]:  # assign user role to new users only
        user = kwargs["instance"]
        assign_role(user, "regular_user")
