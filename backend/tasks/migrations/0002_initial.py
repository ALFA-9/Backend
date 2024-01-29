# Generated by Django 4.2.9 on 2024-01-26 17:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tasks", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comment_employee",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comment_task",
                to="tasks.task",
                verbose_name="Задача",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="task",
            unique_together={("name", "idp")},
        ),
    ]
