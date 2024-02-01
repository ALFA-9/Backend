from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from users.models import Employee


@pytest.mark.django_db
def test_user_auth(client: APIClient, create_employees_for_director_1):
    user = Employee.objects.get(id=1)
    url = "/api/auth/"
    data = {"email": user.email}
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.OK
    assert response.json().get("token")


@pytest.mark.django_db
def test_api_endpoint(client: APIClient, create_employees_for_director_1):
    def assert_instances(instances):
        for element in instances:
            assert "id" in element
            assert "first_name" in element
            assert "last_name" in element
            assert "patronymic" in element
            assert "email" in element
            assert "phone" in element
            assert "grade" in element
            assert "post" in element
            assert "department" in element
            assert "is_staff" in element

    client.force_login(Employee.objects.get(id=1))
    url = "/api/employees/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    element = response.json()
    assert isinstance(element, list)
    assert_instances(element)
