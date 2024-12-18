# Generated by Django 4.2.16 on 2024-09-26 11:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.PositiveSmallIntegerField(
                blank=True,
                choices=[
                    (1, "USER"),
                    (2, "MEMBER"),
                    (3, "STAFF"),
                    (4, "MANAGER"),
                    (5, "ADMIN"),
                ],
                null=True,
            ),
        ),
    ]
