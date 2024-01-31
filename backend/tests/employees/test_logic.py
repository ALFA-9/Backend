import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import Employee


@pytest.mark.django_db
def test_create_employee(create_employee):
    # Вызываем фикстуру для создания сотрудника
    employees = create_employee

    # Проверяем, что сотрудник успешно создан в базе данных
    assert Employee.objects.count() == len(employees)

    # Проверяем атрибут director для каждого сотрудника
    for i, employee in enumerate(employees):
        if i > 0:
            assert employee.director == employees[i - 1]
        else:
            assert employee.director is None


@pytest.mark.django_db
def test_auth_api_view(create_employee):
    client = APIClient()
    # Получаем пользователя из фикстуры
    employee = create_employee[0]

    url = reverse("registration")
    data = {"email": employee.email}
    response = client.post(url, data, format="json")

    # Проверяем, что ответ имеет статус 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Проверяем, что в ответе есть ключ "token"
    assert "token" in response.data

    # Проверяем, что токен существует в базе данных
    token_key = response.data["token"]
    assert Employee.objects.filter(auth_token__key=token_key).exists()


@pytest.mark.django_db
def test_some_scenario(create_employee_with_tokens):
    employee_data = create_employee_with_tokens
