import csv

from django.core.management.base import BaseCommand

from users.models import Department, Employee, Grade, Post, User


class Command(BaseCommand):
    help = "import data from employee.csv"

    def handle(self, *args, **kwargs):
        with open("data/new_employee.csv", encoding="utf8") as f:
            reader_object = csv.reader(f, delimiter=",")
            next(reader_object, None)
            for row in reader_object:
                user_id = row[1]
                user = User.objects.get(id=user_id)
                grade_id = row[7]
                grade = Grade.objects.get(id=grade_id)
                post_id = row[8]
                post = Post.objects.get(id=post_id)
                department_id = row[9]
                department = Department.objects.get(id=department_id)
                obj = Employee(
                    id=row[0],
                    user=user,
                    last_name=row[2],
                    first_name=row[3],
                    patronymic=row[4],
                    phone=row[6],
                    grade=grade,
                    post=post,
                    department=department,
                )
                obj.save()

                # Обновление User employee через related_name
                user.user = obj
                user.save()

                # Загрузка руководителей и создание связей
                director_id = row[10]
                if director_id:
                    director = Employee.objects.get(id=director_id)
                    obj.director = director
                    obj.save()
