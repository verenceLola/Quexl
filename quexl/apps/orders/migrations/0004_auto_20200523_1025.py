# Generated by Django 2.2.10 on 2020-05-23 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_auto_20200506_0953"),
    ]

    operations = [
        migrations.AlterField(
            model_name="history",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="history",
            name="output_url",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
