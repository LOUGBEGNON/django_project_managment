# Generated by Django 4.2.16 on 2024-11-23 11:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0019_remove_task_prerequisites"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="prerequisites",
            field=models.ManyToManyField(
                related_name="subsequent_tasks", to="dashboard.task"
            ),
        ),
    ]
