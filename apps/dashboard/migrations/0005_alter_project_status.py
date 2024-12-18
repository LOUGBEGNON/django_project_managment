# Generated by Django 4.2.16 on 2024-09-27 04:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0004_alter_project_complete_percentage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="status",
            field=models.CharField(
                choices=[
                    (0, "CREATED"),
                    (1, "IN PROGRESS"),
                    (2, "PAUSED"),
                    (3, "COMPLETED"),
                ],
                default=(0, "CREATED"),
                max_length=7,
            ),
        ),
    ]
