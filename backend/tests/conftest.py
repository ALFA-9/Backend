import datetime as dt

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from idps.models import Idp
from tasks.models import Task, TaskControl, TaskType
from users.models import Department, Employee, Grade, Post


@pytest.fixture
def create_employee():
    grades = [Grade.objects.create(title=f"Grade{i}") for i in range(1, 6)]
    posts = [Post.objects.create(title=f"Post{i}") for i in range(1, 6)]
    departments = [
        Department.objects.create(title=f"Department{i}") for i in range(1, 6)
    ]
    TaskType.objects.create(
        name="Project",
    )
    TaskControl.objects.create(
        title="Test",
    )
    employee_list = []
    for i in range(1, 6):
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
    )
    return Task.objects.create(
        name="Test task",
        idp=idp,
        description="New test",
        type=TaskType.objects.get(id=1),
        control=TaskControl.objects.get(id=1),
        date_end=date_end,
    )
