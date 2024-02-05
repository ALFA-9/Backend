import datetime as dt
from http import HTTPStatus

import pytest
from django.utils.translation import gettext_lazy as _
from rest_framework.test import APIClient

from users.models import Employee


@pytest.mark.django_db
def test_post_idp(client: APIClient, create_employee):
    client.force_login(Employee.objects.get(id=1))
    url = "/api/v1/idps/"
    date_start = dt.date.today()
    date_end = date_start + dt.timedelta(days=180)
    data = {
        "title": "Title",
        "employee": 3,
        "tasks": [
            {
                "name": "Task",
                "description": "First task",
                "date_start": date_start.strftime("%d.%m.%Y"),
                "date_end": date_end.strftime("%d.%m.%Y"),
                "type": 1,
                "control": 1,
            }
        ],
    }
    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "title": "Title",
        "employee": 3,
        "director": 1,
        "status_idp": "in_work",
        "tasks": [
            {
                "id": 1,
                "name": "Task",
                "description": "First task",
                "date_start": date_start.strftime("%d.%m.%Y"),
                "date_end": date_end.strftime("%d.%m.%Y"),
                "type": 1,
                "control": 1,
                "status_progress": "in_work",
                "is_completed": False,
            }
        ],
    }

    client.force_login(Employee.objects.get(id=4))
    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        "error": "Вы не являетесь начальником для этого сотрудника."
    }


@pytest.mark.django_db
def test_patch_idp(client: APIClient, create_task):
    client.force_login(Employee.objects.get(id=1))
    url = "/api/v1/idps/1/"
    data = {
        "status_idp": "done",
    }

    response = client.patch(url, data, "application/json")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == data


@pytest.mark.django_db
def test_incorrect_user_patch_idp(client: APIClient, create_task):
    client.force_login(Employee.objects.get(id=2))
    url = "/api/v1/idps/1/"
    data = {
        "status_idp": "done",
    }

    response = client.patch(url, data, "application/json")
    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.django_db
def test_post_idp_when_emp_have_active(client: APIClient, create_task):
    client.force_login(Employee.objects.get(id=1))
    url = "/api/v1/idps/"
    date_start = dt.date.today()
    date_end = date_start + dt.timedelta(days=180)
    data = {
        "title": "Title",
        "employee": 4,
        "tasks": [
            {
                "name": "Task",
                "description": "First task",
                "date_start": date_start.strftime("%d.%m.%Y"),
                "date_end": date_end.strftime("%d.%m.%Y"),
                "type": 1,
                "control": 1,
            }
        ],
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"error": "У этого сотрудника уже есть активный ИПР."}


@pytest.mark.django_db
def test_post_incorrect_idp(
    client: APIClient,
    create_employee,
):
    client.force_login(Employee.objects.get(id=1))
    date_start = dt.date.today()
    date_end = date_start - dt.timedelta(days=1)
    url = "/api/v1/idps/"
    data = {
        "employee": 4,
        "title": "Title",
        "tasks": [
            {
                "name": "Task",
                "description": "First task",
                "date_start": date_start.strftime("%d.%m.%Y"),
                "date_end": date_end.strftime("%d.%m.%Y"),
                "type": 1,
                "control": 1,
            }
        ],
    }
    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "tasks": ["Дата окончания должна быть больше даты начала."],
    }

    data.pop("title")
    data["tasks"][0]["date_start"] = date_end.strftime("%d.%m.%Y")
    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "title": [_("Обязательное поле.")],
        "tasks": ["Нельзя создать задачу задним числом."],
    }


@pytest.mark.django_db
def test_api_endpoint(client: APIClient, create_task):
    client.force_login(Employee.objects.get(id=4))
    url = "/api/v1/idps/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)
    for element in response.json():
        assert "id" in element
        assert "title" in element
        assert "director" in element
        assert "status_idp" in element
        assert "progress" in element

        assert "id" in element["current_task"]
        assert "name" in element["current_task"]
        assert "date_end" in element["current_task"]


@pytest.mark.django_db
def test_idp_request(client: APIClient, create_employee):
    client.force_login(Employee.objects.get(id=2))
    url = "/api/v1/request/"
    data = {
        "title": "New IDP",
        "letter": "I need it",
        "director_id": 1,
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "title": "New IDP",
        "letter": "I need it",
        "director_id": 1,
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.TOO_MANY_REQUESTS
    assert response.json() == {
        "error": "Запрос можно отправлять не чаще 1 раза в сутки."
    }


@pytest.mark.django_db
def test_idp_request_with_active_idp(client: APIClient, create_task):
    client.force_login(Employee.objects.get(id=4))
    url = "/api/v1/request/"
    data = {
        "title": "New IDP",
        "letter": "I need it",
        "director_id": 1,
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "error": "Нельзя запросить ИПР, пока не завершено текущее."
    }


@pytest.mark.django_db
def test_idp_request_incorrect_director(client: APIClient, create_employee):
    client.force_login(Employee.objects.get(id=2))
    url = "/api/v1/request/"
    data = {
        "title": "New IDP",
        "letter": "I need it",
        "director_id": 3,
    }

    response = client.post(url, data, "application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "error": "Вы не можете отправить запрос данному сотруднику."
    }
