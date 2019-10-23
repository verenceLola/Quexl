# Generated by Django 2.2.6 on 2019-11-14 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profiles", "0003_auto_20191029_0619")]

    operations = [
        migrations.RemoveField(model_name="education", name="on_going"),
        migrations.RemoveField(model_name="workexperience", name="on_going"),
        migrations.AlterField(
            model_name="education",
            name="level",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Secondary School", "Sec"),
                    ("Diploma", "Dip"),
                    ("Degree", "Deg"),
                    ("PHD", "Phd"),
                    ("Masters", "Mas"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="skill",
            name="expertise",
            field=models.CharField(
                choices=[
                    ("beginner", "B"),
                    ("intermediate", "I"),
                    ("expert", "E"),
                ],
                max_length=15,
            ),
        ),
    ]