# Generated by Django 2.2.8 on 2020-03-16 09:27

from decimal import Decimal

import djmoney.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0009_auto_20200316_0915"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="price",
            field=djmoney.models.fields.MoneyField(
                decimal_places=4,
                default=Decimal("0.0"),
                default_currency="USD",
                max_digits=19,
            ),
        ),
    ]
