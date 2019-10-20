import logging

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models import Q
from django.utils.translation import pgettext_lazy
from django_countries.fields import CountryField
from .validators import validate_possible_number
from phonenumber_field.modelfields import PhoneNumberField
from quexl.helpers.fancy_generator import fancy_id_generator

# Get an instance of a logger
logger = logging.getLogger(__name__)


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


class Address(models.Model):
    id = models.CharField(
        db_index=True,
        max_length=256,
        default=fancy_id_generator,
        primary_key=True,
        editable=False,
    )
    street_address_1 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    city_area = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = CountryField()
    country_area = models.CharField(max_length=128, blank=True)
    phone = PossiblePhoneNumberField(blank=True, default="")

    class Meta:
        ordering = ("pk",)

    @property
    def address(self):
        return "%s" % self.city

    def __repr__(self):
        return (
            "Address(street_address_1=%r, "
            "city=%r, postal_code=%r, country=%r, "
            "country_area=%r, phone=%r)"
            % (
                self.street_address_1,
                self.city,
                self.postal_code,
                self.country,
                self.country_area,
                self.phone,
            )
        )


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
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

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

    @property
    def name(self):
        """
        Return users full names
        """
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
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
