# Generated by Django 2.2.10 on 2020-03-31 11:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models

import quexl.helpers.fancy_generator


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0005_auto_20200331_0841"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={},
        ),
        migrations.AlterUniqueTogether(
            name="comment",
            unique_together=set(),
        ),
        migrations.CreateModel(
            name="Reply",
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
                ("body", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="blog.Comment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="comment",
            name="level",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="lft",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="parent",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="rght",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="tree_id",
        ),
    ]
