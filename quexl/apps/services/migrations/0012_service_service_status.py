# Generated by Django 2.2.10 on 2020-07-13 11:40

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0011_auto_20200330_1324"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="service_status",
            field=models.CharField(
                choices=[
                    ("10", "Start"),
                    ("20", "Exceptions"),
                    ("30", "Success"),
                ],
                default="10",
                max_length=10,
            ),
        ),
    ]
