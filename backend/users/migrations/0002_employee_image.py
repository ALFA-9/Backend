# Generated by Django 4.2.9 on 2024-02-02 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='profiles/', verbose_name='Фото'),
        ),
    ]
