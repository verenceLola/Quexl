# Generated by Django 2.2.8 on 2019-12-12 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("messaging", "0004_auto_20191205_1059")]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="sent_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        )
    ]