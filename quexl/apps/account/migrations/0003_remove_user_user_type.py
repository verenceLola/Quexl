# Generated by Django 2.2.10 on 2020-04-17 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_user_user_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="user_type",
        ),
    ]
