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
                user_id = row[0]
                user = User.objects.get(id=user_id)
                grade_id = row[6]
                grade = Grade.objects.get(id=grade_id)
                post_id = row[7]
                post = Post.objects.get(id=post_id)
                department_id = row[8]
                department = Department.objects.get(id=department_id)
                obj = Employee(
                    user=user,
                    last_name=row[1],
                    first_name=row[2],
                    patronymic=row[3],
                    phone=row[5],
                    grade=grade,
                    post=post,
                    department=department,
                )
                obj.save()

                # Обновление employee через related_name User
                user.user = obj
                user.save()

                # # Загрузка руководителей и создание связей
                # director_id = row[9]
                # if director_id:
                #     # director, created = Employee.objects.get_or_create(
                #     # user=director_name
                #     # )
                #     # Сохраняем связь между ID сотрудника и руководителя
                #     # directors[row[0]] = director
                #     obj.director = director_id
                #     obj.save()
