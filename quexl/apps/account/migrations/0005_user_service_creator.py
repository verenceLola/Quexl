# Generated by Django 2.2.10 on 2020-05-22 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_auto_20200507_0948"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="service_creator",
            field=models.BooleanField(default=False),
        ),
    ]
