# Generated by Django 2.2.6 on 2019-12-02 12:01

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("messaging", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="thread",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        )
    ]
