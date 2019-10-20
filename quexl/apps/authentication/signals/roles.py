"""
signal to add regular user role to every new user
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from quexl.apps.authentication.models import User
from rolepermissions.roles import assign_role


@receiver(post_save, sender=User)
def add_regular_user_role(sender, **kwargs):
    if kwargs["created"]:  # assign user role to new users only
        user = kwargs["instance"]
        assign_role(user, "regular_user")
