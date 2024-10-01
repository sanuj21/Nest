# Generated by Django 5.1.1 on 2024-10-01 16:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("github", "0010_alter_repositorycontributor_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="repository",
            name="funding_yml",
            field=models.JSONField(blank=True, default=dict, verbose_name="FUNDING.yml data"),
        ),
        migrations.AlterField(
            model_name="repository",
            name="homepage",
            field=models.CharField(
                blank=True, default="", max_length=100, verbose_name="Homepage"
            ),
        ),
        migrations.AlterField(
            model_name="repository",
            name="pages_status",
            field=models.CharField(
                blank=True, default="", max_length=20, verbose_name="Pages status"
            ),
        ),
    ]
