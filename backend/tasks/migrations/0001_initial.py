# Generated by Django 4.2.9 on 2024-01-26 17:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('idps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=500, verbose_name='Комментарий')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='Метод контроля выполнения задачи')),
            ],
            options={
                'verbose_name': 'Метод контроля',
                'verbose_name_plural': 'Методы контроля',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название типа задачи')),
            ],
            options={
                'verbose_name': 'Тип задачи',
                'verbose_name_plural': 'Типы задач',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название задачи')),
                ('description', models.TextField(max_length=500, verbose_name='Описание задачи')),
                ('status_progress', models.CharField(choices=[('in_work', 'в работе'), ('done', 'выполнено')], default='in_work', max_length=20, verbose_name='Статус выполнения')),
                ('status_accept', models.CharField(choices=[('accepted', 'принято'), ('not_accepted', 'не принято'), ('cancelled', 'отменено')], default='not_accepted', max_length=20, verbose_name='Статус проверки')),
                ('date_start', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата начала выполнения задачи')),
                ('date_end', models.DateTimeField(verbose_name='Дата окончания выполнения задачи')),
                ('control', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_control', to='tasks.control', verbose_name='Метод контроля выполнения задачи')),
                ('idp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_idp', to='idps.idp', verbose_name='ИПС')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_type', to='tasks.type', verbose_name='Тип задачи')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'ordering': ('id',),
            },
        ),
    ]
