# Generated by Django 2.2.10 on 2020-03-31 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_auto_20200331_1101"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Reply",
        ),
    ]
