# Generated by Django 2.2.8 on 2020-03-28 07:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("contact", "0002_auto_20200328_0740"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contact",
            name="resolved",
        ),
    ]
