import csv

from django.core.management.base import BaseCommand

from tasks.models import Type


class Command(BaseCommand):
    help = "import data from type.csv"

    def handle(self, *args, **kwargs):
        with open("data/type.csv", encoding="utf8") as f:
            reader_object = csv.reader(f, delimiter=",")
            next(reader_object, None)
            for row in reader_object:
                obj = Type(
                    id=row[0],
                    name=row[1],
                )
                obj.save()
