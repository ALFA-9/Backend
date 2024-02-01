import datetime as dt

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from idps.models import Idp
from tasks.models import Control, Task, Type
from users.models import Department, Employee, Grade, Post


@pytest.fixture
def create_employee():
    grades = [Grade.objects.create(title=f"Grade{i}") for i in range(1, 5)]
    posts = [Post.objects.create(title=f"Post{i}") for i in range(1, 5)]
    departments = [
        Department.objects.create(title=f"Department{i}") for i in range(1, 5)
    ]
    employee_list = []
    for i in range(1, 5):
        employee = Employee.objects.create(
            first_name=f"Иван{i}",
            last_name=f"Иванов{i}",
            patronymic=f"Иванович{i}",
            email=f"ivan.ivanov{i}@example.com",
            phone=f"7 (917) 123-45-6{i}",
            grade=grades[i - 1],
            post=posts[i - 1],
            department=departments[0],
            is_staff=False,
        )

        # Устанавливаем атрибут director для иерархической структуры
        if i > 1:
            employee.director = employee_list[i - 2]
            employee.save()

        employee_list.append(employee)
    return employee_list


@pytest.fixture
def token_user(employee):
    # Создаем токен для пользователя
    token = Token.objects.create(email=employee.email)
    return {"token": str(token)}


@pytest.fixture
def create_employee_with_tokens(create_employee):
    employees = create_employee
    for employee in employees:
        client = APIClient()
        # Создаем токены для каждого сотрудника
        url = reverse("registration")
        data = {"email": employee.email}
        client.post(url, data, format="json")

    return {"employees": employees}


@pytest.fixture
def create_multiple_directors():
    for dir in range(1, 4):
        Employee.objects.create(
            first_name=f"Emp{dir}",
            email=f"email{dir}@dir.com",
            phone=f"7 (999) 99{dir}-00-00",
        )


@pytest.fixture
def create_employees_for_director_1(create_multiple_directors):
    for emp in range(1, 4):
        Employee.objects.create(
            first_name=f"Emp1-{emp}",
            email=f"email1-{emp}@dir.com",
            phone=f"7 (999) 991-{emp}0-00",
            director=Employee.objects.get(id=1),
        )


@pytest.fixture
def create_idp(create_employees_for_director_1):
    date_start = dt.date.today()
    date_end = date_start + dt.timedelta(days=180)
    return Idp.objects.create(
        title="Title",
        employee=Employee.objects.get(id=4),
        director=Employee.objects.get(id=1),
        status_idp="in_work",
        date_end=date_end,
    )


@pytest.fixture
def create_task(db, create_employee):
    date_start = dt.date.today()
    date_end = date_start + dt.timedelta(days=180)
    # Используем фикстуру create_employee
    employees = create_employee
    employee = employees[3]
    director = employees[0]
    # Выбираем одного из созданных сотрудников
    idp = Idp.objects.create(
        title="Test idp",
        employee=employee,
        director=director,
        status_idp="in_work",
        date_end=date_end,
    )
    type = Type.objects.create(
        name="Project",
    )
    control = Control.objects.create(
        title="Test",
    )
    return Task.objects.create(
        name="Test task",
        idp=idp,
        description="New test",
        type=type,
        control=control,
        date_end=date_end,
    )
