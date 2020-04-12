from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Q
from django.utils.translation import pgettext_lazy
from djmoney.models.fields import MoneyField

from quexl.helpers.fancy_generator import fancy_id_generator


class UserManager(BaseUserManager):
    def create_user(
        self, username, email, password=None, is_staff=False, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        if username is None:
            raise TypeError("Users must have a username.")

        # Google OAuth2 backend send unnecessary username field
        extra_fields.pop("username", None)

        if email is None:
            raise TypeError("Users must have an email address.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save()

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def regular_user(self):
        return self.get_queryset().filter(
            Q(is_staff=False) | (Q(is_staff=True))
        )

    def staff(self):
        return self.get_queryset().filter(is_staff=True)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=False)
    date_of_joining = models.DateTimeField(auto_now_add=True)
    linked_accounts = models.CharField(
        max_length=30, null=True
    )  # TODO implement as required
    is_staff = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    balance = MoneyField(
        max_digits=19, decimal_places=4, default=0.0000, default_currency="USD"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    class Meta:
        permissions = (
            (
                "manage_users",
                pgettext_lazy(
                    "Permission description", "Manage regular users."
                ),
            ),
            (
                "manage_staff",
                pgettext_lazy("Permission description", "Manage staff."),
            ),
            (
                "impersonate_users",
                pgettext_lazy("Permission description", "Impersonate users."),
            ),
        )

    def __str__(self):
        """
        Returns a string representation of this `User`.
        """
        return self.username

    @staticmethod
    def get_user(email):
        try:
            user = User.objects.get(email=email)
            return user

        except Exception:
            return False

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = User.objects.get(id=user_id)
            return user

        except Exception:
            return False
