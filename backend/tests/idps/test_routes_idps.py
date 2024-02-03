from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from users.models import Employee


@pytest.mark.django_db
def test_api_endpoint(client: APIClient, create_employee):
    client.force_login(Employee.objects.get(id=1))
    response = client.get("/api/idps/")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_api_endpoint_by_id(client: APIClient, create_task):
    client.force_login(Employee.objects.get(id=1))
    response = client.get("/api/idps/1/")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_api_endpoint_by_id_not_director(client: APIClient, create_task):
    client.force_login(Employee.objects.get(id=5))
    response = client.get("/api/idps/1/")
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_idp_by_not_exists_id(client: APIClient, create_task):
    client.force_login(Employee.objects.get(id=1))
    response = client.get("/api/idps/2/")
    assert response.status_code == HTTPStatus.NOT_FOUND
