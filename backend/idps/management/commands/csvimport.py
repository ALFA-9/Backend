"""
Реализация management-комманды импорта из csv в БД.

Модуль умеет автоматически проводить анализ всех моделей проекта и сопоставлять
их по именам соответствующим файлам. Имеет анализ внешних ключей и начинает
импорт с таблиц без внешних связей. Таким образом разрешаются проблемы
целостности БД, которые возможны при прямой записи в БД.
Может быть использован и отдельно в других проектах на DRF.

Запуск:
manage.py csvimport [-h] [-f FILE] [-m MODEL] [-d DIR] [-is] [-c] [-r]
"""

import csv
import os
import re

import django.apps
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

PLURAL_REGEXP = '({model}?)(es|s)$'


class Command(BaseCommand):
    """Модуль импорта из csv-файлов в Django."""

    def add_arguments(self, parser):
        """Регистрируем ключи запуска."""
        parser.add_argument('-f', '--file', type=str, help='Файл для импорта')
        parser.add_argument(
            '-m',
            '--model',
            type=str,
            help='Модель для импорта',
        )
        parser.add_argument('-d', '--dir', help='Директория для импорта')
        parser.add_argument(
            '-is',
            '--ignore_s',
            action='store_true',
            help=(
                'Игнорирование множественного ',
                'числа в английском названии файла',
            ),
        )
        parser.add_argument(
            '-c',
            '--clear',
            action='store_true',
            help=('Очистить модель перед импортом'),
        )
        parser.add_argument(
            '-r',
            '--recurse',
            action='store_true',
            help='Рекурсивный просмотр директории',
        )

    def handle(self, *args, **kwargs):
        """Начало команды."""
        self.import_file = kwargs.get('file')
        self.import_model = kwargs.get('model')
        self.import_dir = kwargs.get('dir')
        self.import_clear_model = kwargs.get('clear')
        self.import_ignore_s = kwargs.get('ignore_s')
        self.import_recurse = kwargs.get('recurse')
        self.model_list = django.apps.apps.get_models(
            include_auto_created=True,
        )
        self.check_command()
        if self.import_file:
            self.file_import()
        elif self.import_dir:
            self.dir_import()

    def find_model(self, filename=None, modelname=None, silent=False):
        """Поиск модели по названию или имени файла с учётом ключей запуска."""
        model = None
        if filename:
            modelname = os.path.basename(filename).split('.')[0]
        elif not modelname:
            print("Не указаны ни файл, ни модель")
        # Ищем модель по имени
        for current_model in self.model_list:
            if (
                modelname.lower()
                == current_model.__name__.lower()
            ) or (
                modelname.lower().replace('_', '')
                == current_model.__name__.lower()
            ) or (
                modelname.lower().replace('-', '')
                == current_model.__name__.lower()
            ):
                model = current_model
        # Ищем модель по имени игнорируя множественное число
        if not model and self.import_ignore_s:
            for current_model in self.model_list:
                pattern = re.compile(
                    PLURAL_REGEXP.format(
                        model=current_model.__name__.lower(),
                    ),
                )
                if pattern.match(modelname.lower()):
                    model = current_model
        if not model and not silent:
            print(
                'Невозможно получить имя модели по имени файла. ',
                'Используйте аргумент -m <model_name>, ',
                'или -is, если в названии файла присутствует ',
                'множественное число.',
            )
        return model

    def check_command(self):
        """Проверка совместимости ключей запуска."""
        if self.import_file and self.import_dir:
            print('Можно задать либо файл, либо директорию')
            exit(-1)
        if self.import_file and self.import_recurse:
            print('Ключ \"--recurse\" применим только к папкам')
            exit(-1)
        if self.import_model and self.import_dir:
            print('Ключ \"--model\" применим только к файлам')
            exit(-1)
        if not self.import_file and not self.import_dir:
            print('Должны быть указаны либо папка, либо файл')
            exit(-1)

    def file_import(self):
        """Импорт из конкретного файла."""
        if os.path.exists(self.import_file):
            splitted_filename = os.path.basename(
                self.import_file,
            ).split('.')
            if splitted_filename[1] != 'csv':
                print('Поддерживаются только csv файлы.')
                return
            else:
                if (
                    self.import_model
                    and (
                        model := self.find_model(
                            modelname=self.import_model,
                        )
                    )
                ):
                    self.file_model = {self.import_file: model}
                    self.import_from_file(
                        self.import_file,
                    )
                    return
                elif self.import_model:
                    print('Модель не найдена в проекте.')
                    return
                if model := self.find_model(
                        filename=self.import_file,
                ):
                    print(f'Импорт в модель {model.__name__}')
                    self.file_model = {self.import_file: model}
                    self.import_from_file(
                        self.import_file,
                    )
        else:
            print(f'Файл {self.import_file} не существует.')
            return

    def dir_import(self):
        """Импорт из директории."""
        file_list = self.get_file_list(self.import_dir)
        file_model = dict()
        for file in file_list:
            model = self.find_model(filename=file, silent=True)
            if model:
                file_model[file] = model
        for current_file in file_model.keys():
            if not file_model.get(current_file):
                del file_model[current_file]
        self.file_model = file_model
        self.import_dispatcher()

    def import_dispatcher(self):
        """Выдает файл на парсинг, кроме уже импортированных."""
        files = list(self.file_model.keys())
        for current_file in files:
            if self.file_model.get(current_file):
                self.import_from_file(current_file)

    def get_file_list(self, dir):
        """Получение списка csv файлов из директории."""
        file_list = []
        dir_list = []
        with os.scandir(dir) as dir_items:
            for item in dir_items:
                if item.is_file():
                    if item.name.split('.')[1] == 'csv':
                        file_list.append(item.path)
                elif item.is_dir():
                    dir_list.append(item)
        if (self.import_recurse):
            for dir in dir_list:
                file_list.extend(self.get_file_list(dir))
        return file_list

    def _prepare_field_value(self, model_fields):
        field_value = dict()
        for field in model_fields:
            # if field.__class__.__name__ == 'ForeignKey':
            #     femote_field = field.remote_field.model
            #     if femote_field in self.file_model.values():
            #         for tfile in self.file_model.keys():
            #             if femote_field == self.file_model[tfile]:
            #                 self.import_from_file(tfile)
            #                 break
            name = field.name
            field_value[name] = None
        return field_value

    def _filling_field_value(self, row, model_fields, field_value):
        for field in model_fields:
            # Получаем имя поля, ожидаемое в csv (имя столбца БД)
            fname = field.db_column or field.attname
            # Заполняем значениями по-умолчанию или из файла, если есть
            field_value[fname] = row.get(fname) or field.get_default()
            if (
                field.__class__.__name__ == 'ForeignKey'
            ):
                try:
                    field_value[field.name] = (
                        field.remote_field.model.objects.get(
                            pk=int(row[fname]),
                        )
                    )
                except ObjectDoesNotExist:
                    print(
                        'Есть поле, которое невозможно заполнить',
                        'данными из связанной таблицы',
                    )
                    print('Пропущено')
                    continue
        return field_value

    def import_from_file(self, file):
        """Непосредственно импорт из файла."""
        model = self.file_model[file]
        if self.import_clear_model:
            model.objects.all().delete()
        model_fields = model._meta.fields
        field_value = self._prepare_field_value(model_fields)
        print('\n' + file + ' >', model.__name__)
        with open(file, 'r', encoding='utf-8') as csvfile:
            filereader = csv.DictReader(csvfile)
            print(f'Поля файла: {filereader.fieldnames}')
            print(f'Поля модели: {set(field_value.keys())}')
            for row in filereader:
                print('Импротируем:', list(row.values()))
                field_value = self._filling_field_value(
                    row,
                    model_fields,
                    field_value,
                )
                try:
                    model.objects.update_or_create(**field_value)
                except ValueError:
                    print('Невозможно создать объект с такими данными')
                    print('Пропущено')
                    continue
                except IntegrityError as e:
                    print(f'Ошибка импорта в таблицу: {e}')
                    break
        # Удаляем из словаря импортированный файл
        del self.file_model[file]
        return
