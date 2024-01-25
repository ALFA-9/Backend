import csv

from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "import data from user.csv"

    def handle(self, *args, **kwargs):
        with open("data/user.csv", encoding="utf8") as f:
            reader_object = csv.reader(f, delimiter=",")
            next(reader_object, None)
            for row in reader_object:
                obj = User(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    password=row[3],
                )
                obj.save()
