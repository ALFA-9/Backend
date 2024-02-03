from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from users.models import Employee


@pytest.mark.django_db
def test_user_auth(client: APIClient, create_employee):
    user = Employee.objects.get(id=1)
    url = "/api/auth/"
    data = {"email": user.email}
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.OK
    assert response.json().get("token")


@pytest.mark.django_db
def test_api_endpoint_get_subordinates(client: APIClient, create_task):
    def assert_instances(instances):
        for element in instances:
            assert "id" in element
            assert "first_name" in element
            assert "last_name" in element
            assert "patronymic" in element
            assert "post" in element
            assert "subordinates" in element

    client.force_login(Employee.objects.get(id=3))
    url = "/api/employees/get_subordinates/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    element = response.json()
    assert_instances(element["subordinates"])


@pytest.mark.django_db
def test_api_endpoint_me(client: APIClient, create_task):
    def assert_instances(instances):
        for element in instances:
            assert "id" in element
            assert "progress" in element
            assert "title" in element
            assert "status_idp" in element
            assert "director" in element

            assert "id" in element["current_task"]
            assert "date_end" in element["current_task"]
            assert "name" in element["current_task"]

    client.force_login(Employee.objects.get(id=4))
    url = "/api/employees/me/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    element = response.json()
    assert_instances(element["idps"])
