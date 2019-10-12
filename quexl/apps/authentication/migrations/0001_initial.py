# Generated by Django 2.2.6 on 2019-10-05 05:45

from django.db import migrations, models
import django_countries.fields
import quexl.apps.authentication.models
import quexl.helpers.fancy_generator


class Migration(migrations.Migration):

    initial = True

    dependencies = [("auth", "0011_update_proxy_permissions")]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.CharField(
                        db_index=True,
                        default=quexl.helpers.fancy_generator.fancy_id_generator,
                        editable=False,
                        max_length=256,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "street_address_1",
                    models.CharField(blank=True, max_length=256),
                ),
                ("city", models.CharField(blank=True, max_length=256)),
                ("city_area", models.CharField(blank=True, max_length=128)),
                ("postal_code", models.CharField(blank=True, max_length=20)),
                (
                    "country",
                    django_countries.fields.CountryField(max_length=2),
                ),
                ("country_area", models.CharField(blank=True, max_length=128)),
                (
                    "phone",
                    quexl.apps.authentication.models.PossiblePhoneNumberField(
                        blank=True, default="", max_length=128, region=None
                    ),
                ),
            ],
            options={"ordering": ("pk",)},
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "password",
                    models.CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "id",
                    models.CharField(
                        db_index=True,
                        default=quexl.helpers.fancy_generator.fancy_id_generator,
                        editable=False,
                        max_length=256,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        db_index=True, max_length=255, unique=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        db_index=True, max_length=254, unique=True
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=256)),
                ("last_name", models.CharField(blank=True, max_length=256)),
                ("is_active", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("date_of_joining", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "permissions": (
                    ("manage_users", "Manage regular users."),
                    ("manage_staff", "Manage staff."),
                    ("impersonate_users", "Impersonate users."),
                )
            },
        ),
    ]
