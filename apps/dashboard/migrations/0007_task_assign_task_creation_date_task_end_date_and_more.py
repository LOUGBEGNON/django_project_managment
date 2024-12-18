# Generated by Django 4.2.16 on 2024-09-27 05:47

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0006_alter_project_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assign',
            field=models.ManyToManyField(related_name='assign_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='creation_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='end_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='task',
            name='start_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='task',
            name='update_date',
            field=models.DateField(auto_now=True),
        ),
    ]
