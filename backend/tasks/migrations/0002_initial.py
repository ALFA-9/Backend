# Generated by Django 4.2.9 on 2024-02-02 16:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tasks", "0001_initial"),
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
