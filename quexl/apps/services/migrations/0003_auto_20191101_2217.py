# Generated by Django 2.2.6 on 2019-11-01 22:17

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("services", "0002_auto_20191101_1803")]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="buyer_requirements",
            new_name="details",
        ),
        migrations.RenameField(
            model_name="order", old_name="amount", new_name="price"
        ),
        migrations.RenameField(
            model_name="order",
            old_name="amount_currency",
            new_name="price_currency",
        ),
        migrations.AlterField(
            model_name="order",
            name="attachment",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.URLField(null=True), default=list, size=5
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="buyer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_buyer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="number_of_revisions",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_type",
            field=models.CharField(
                choices=[
                    ("offer", "order offer"),
                    ("proposal", "order proposal"),
                ],
                default="offer",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="seller",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_seller",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
