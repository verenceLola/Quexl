"""
signal to create user profile upon user activation
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from quexl.apps.account.models import User
from quexl.apps.profiles.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    """
    create user profile when user account is activated
    """
    user = kwargs["instance"]

    if kwargs["created"]:
        Profile.objects.create(user=user)
