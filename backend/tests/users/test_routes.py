from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from users.models import Employee


@pytest.mark.django_db
def test_api_employees(client: APIClient, create_employees_for_director_1):
    client.force_login(Employee.objects.get(id=1))
    response = client.get("/api/employees/")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_api_employees_by_id(
    client: APIClient, create_employees_for_director_1
):
    client.force_login(Employee.objects.get(id=1))
    response = client.get("/api/employees/1/")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_api_employees_by_id_not_director(
    client: APIClient, create_employees_for_director_1
):
    client.force_login(Employee.objects.get(id=2))
    response = client.get("/api/employees/1/")
    assert response.status_code == HTTPStatus.FORBIDDEN
