# Generated by Django 4.2.16 on 2024-09-27 15:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_alter_task_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='creation_date',
            field=models.DateTimeField(blank=True, db_index=True, default=django.utils.timezone.now, help_text='Creation date, by default it is now.', verbose_name='creation date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='end_date',
            field=models.DateField(blank=True, db_index=True, default=django.utils.timezone.now, help_text='End date, by default it is now.', verbose_name='end date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateField(blank=True, db_index=True, default=django.utils.timezone.now, help_text='Start date, by default it is now.', verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='task',
            name='update_date',
            field=models.DateField(blank=True, db_index=True, default=django.utils.timezone.now, help_text='Update date, by default it is now.', verbose_name='update date'),
        ),
    ]
