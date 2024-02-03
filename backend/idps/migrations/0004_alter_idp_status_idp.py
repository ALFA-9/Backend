# Generated by Django 4.2.9 on 2024-02-03 10:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("idps", "0003_remove_idp_date_end_alter_idp_date_start"),
    ]

    operations = [
        migrations.AlterField(
            model_name="idp",
            name="status_idp",
            field=models.CharField(
                choices=[
                    ("in_work", "в работе"),
                    ("cancelled", "отменен"),
                    ("not_completed", "не выполнен"),
                    ("done", "выполнен"),
                ],
                default="in_work",
                max_length=100,
                verbose_name="статус",
            ),
        ),
    ]