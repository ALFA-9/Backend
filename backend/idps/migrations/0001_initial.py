# Generated by Django 4.2.9 on 2024-02-01 19:27

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Idp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=100, verbose_name="название"),
                ),
                (
                    "status_idp",
                    models.CharField(
                        choices=[
                            ("in_work", "в работе"),
                            ("canceled", "отменен"),
                            ("not_completed", "не выполнен"),
                            ("done", "выполнен"),
                        ],
                        default="in_work",
                        max_length=100,
                        verbose_name="статус",
                    ),
                ),
                (
                    "date_start",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата начала"
                    ),
                ),
                ("date_end", models.DateField(verbose_name="дата окончания")),
            ],
            options={
                "verbose_name": "индивидуальный план развития",
                "ordering": ["date_start", "id"],
            },
        ),
    ]
