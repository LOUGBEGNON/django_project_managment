# Generated by Django 4.2.16 on 2024-10-29 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0016_company_responsible"),
        ("authentication", "0003_user_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="employees",
                to="dashboard.company",
            ),
        ),
    ]