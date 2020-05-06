# Generated by Django 2.2.10 on 2020-05-06 09:53

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_auto_20200316_0907"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("PROCESSING", "processing"),
                    ("CANCELLED", "cancelled"),
                    ("COMPLETED", "completed"),
                ],
                default="processing",
                max_length=50,
            ),
        ),
    ]
