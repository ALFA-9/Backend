# Generated by Django 4.2.9 on 2024-01-26 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='username',
            field=models.CharField(null=True),
        ),
    ]
