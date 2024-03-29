# Generated by Django 2.2.10 on 2020-05-25 21:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orders", "0005_datafile_owner"),
    ]

    operations = [
        migrations.RenameField(
            model_name="datafile",
            old_name="owner",
            new_name="file_owner",
        ),
        migrations.AddField(
            model_name="history",
            name="history_owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
