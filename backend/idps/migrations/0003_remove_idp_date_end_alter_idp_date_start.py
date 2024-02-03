# Generated by Django 4.2.9 on 2024-02-02 18:33

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("idps", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="idp",
            name="date_end",
        ),
        migrations.AlterField(
            model_name="idp",
            name="date_start",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="дата начала"
            ),
        ),
    ]