# Generated by Django 4.2.9 on 2024-02-05 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_employee_last_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='email_notifications',
            field=models.TextField(blank=True, null=True),
        ),
    ]
