# Generated by Django 2.2.10 on 2020-07-25 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0006_auto_20200525_2152"),
    ]

    operations = [
        migrations.RemoveField(model_name="order", name="price",),
        migrations.RemoveField(model_name="order", name="price_currency",),
    ]