import datetime as dt
import json
from http import HTTPStatus

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from idps.models import Idp
from tasks.models import Control, Task, Type
from tasks.serializers import TaskSerializer
from users.models import Employee


@pytest.mark.django_db
def test_create_task(create_task):
    task = create_task
    assert isinstance(task, Task)
    assert task.name == "Test task"
    assert task.description == "New test"


@pytest.mark.django_db
def test_post_task(client: APIClient, create_employee):
    client.force_login(Employee.objects.get(id=1))
    employee = Employee.objects.get(id=2)
    director = Employee.objects.get(id=1)
    url = "/api/tasks/"
    date_start = dt.date.today()
    date_end = date_start + dt.timedelta(days=180)
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

    data = {
        "name": "Test task",
        "idp": idp.id,
        "description": "New test",
        "type": type.id,
        "control": control.id,
        "date_end": date_end,
    }
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "name": "Test task",
        "description": "New test",
        "idp": 1,
        "type": {"id": 1, "name": "Project"},
        "status_progress": "in_work",
        "status_accept": "not_accepted",
        "control": {"id": 1, "title": "Test"},
        "date_start": date_start.strftime("%d.%m.%Y"),
        "date_end": date_end.strftime("%d.%m.%Y"),
    }

    client.force_login(Employee.objects.get(id=3))
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"error": "Вы не являетесь автором данного ИПР."}


@pytest.mark.django_db
def test_update_task_status_accept(
    client: APIClient, create_task, create_employee
):
    task = create_task
    # employees = create_employee
    client.force_login(Employee.objects.get(id=1))

    url = f"/api/tasks/{task.id}/"
    data = {"status_accept": "accepted"}

    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK

    # Перезагружаем объект из базы данных, чтобы получить актуальные данные
    task.refresh_from_db()
    # Проверяем, что данные были обновлены
    assert task.status_accept == "accepted"

    client.force_login(Employee.objects.get(id=3))
    data = {"status_accept": "not_accepted"}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Перезагружаем объект из базы данных, чтобы получить актуальные данные
    task.refresh_from_db()
    # Проверяем, что данные не были обновлены
    assert task.status_accept == "accepted"


@pytest.mark.django_db
def test_update_task_status_progress(
    client: APIClient, create_task, create_employee
):
    task = create_task
    client.force_login(Employee.objects.get(id=4))

    url = f"/api/tasks/{task.id}/"
    data = {"status_progress": "done"}

    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK

    # Перезагружаем объект из базы данных, чтобы получить актуальные данные
    task.refresh_from_db()
    # Проверяем, что данные были обновлены
    assert task.status_progress == "done"

    client.force_login(Employee.objects.get(id=2))
    data = {"status_progress": "in_work"}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # Перезагружаем объект из базы данных, чтобы получить актуальные данные
    task.refresh_from_db()
    # Проверяем, что данные не были обновлены
    assert task.status_progress == "done"


@pytest.mark.django_db
def test_delete_task(client: APIClient, create_task, create_employee):
    task = create_task
    client.force_login(Employee.objects.get(id=4))

    response = client.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    client.force_login(Employee.objects.get(id=1))
    response = client.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
