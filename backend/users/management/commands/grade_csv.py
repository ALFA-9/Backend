import csv

from django.core.management.base import BaseCommand

from users.models import Grade


class Command(BaseCommand):
    help = "import data from grade.csv"

    def handle(self, *args, **kwargs):
        with open("data/grade.csv", encoding="utf8") as f:
            reader_object = csv.reader(f, delimiter=",")
            next(reader_object, None)
            for row in reader_object:
                obj = Grade(
                    id=row[0],
                    title=row[1],
                )
                obj.save()