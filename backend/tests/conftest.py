import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import Department, Employee, Grade, Post

# import datetime as dt

# import pytest

# from idps.models import Employee, Idp


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
        response = client.post(url, data, format="json")

    return {"employees": employees}


# @pytest.fixture
# def create_idps_for_emps(create_tree_structure):
#     STATUSES = ["in_work", "canceled", "done"]
#     for i in range(2, 5):
#         emp = Employee.objects.get(id=i)
#         Idp.objects.create(
#             title=f"ИПР для {emp.name}",
#             employee=emp,
#             director=emp.director,
#             date_end=dt.date.today() + dt.timedelta(days=180),
#             status_idp=STATUSES[i - 2],
#         )
#     emp = Employee.objects.get(id=7)
#     Idp.objects.create(
#         title=f"ИПР для {emp.name}",
#         employee=emp,
#         director=emp.director,
#         date_end=dt.date.today() + dt.timedelta(days=180),
#         status_idp="not_completed",
#     )


# @pytest.fixture
# def create_idp_model(create_multiple_employees):
#     date_start = dt.date.today()
#     date_end = date_start + dt.timedelta(days=180)
#     return Idp.objects.create(
#         title="Title",
#         employee=create_multiple_employees[1],
#         director=create_multiple_employees[0],
#         status_idp="in_work",
#         date_end=date_end,
#     )
