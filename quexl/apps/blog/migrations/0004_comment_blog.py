# Generated by Django 2.2.10 on 2020-03-31 08:13

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_auto_20200330_1810"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="blog",
            field=models.ForeignKey(
                default="-M3geV2z57uZ0KSJbMs0",
                on_delete=django.db.models.deletion.CASCADE,
                to="blog.Blog",
            ),
            preserve_default=False,
        ),
    ]
