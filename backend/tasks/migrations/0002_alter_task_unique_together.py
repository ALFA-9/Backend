# Generated by Django 4.2.9 on 2024-01-23 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('name', 'idp')},
        ),
    ]
