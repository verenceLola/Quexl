# Generated by Django 2.2.6 on 2019-10-29 06:19

import django.core.validators
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [("profiles", "0002_auto_20191028_1633")]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="first_name",
            field=models.CharField(
                blank=True,
                max_length=16,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Z]+$",
                        "first name should only have alphabet characters",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="last_name",
            field=models.CharField(
                blank=True,
                max_length=16,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Z]+$",
                        "last name should only have alphabet characters",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
