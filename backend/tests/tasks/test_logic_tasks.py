import datetime as dt
from http import HTTPStatus

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tasks.models import Task
from users.models import Employee


@pytest.mark.django_db
def test_create_task(create_task):
    task = create_task
    assert isinstance(task, Task)
    assert task.name == "Test task"
    assert task.description == "New test"


@pytest.mark.django_db
def test_post_task(client: APIClient, create_task):
    client.force_login(Employee.objects.get(id=1))
    url = "/api/tasks/"
    date_start = dt.date.today()
    date_end = date_start + dt.timedelta(days=180)

    data = {
        "name": "Another test task",
        "idp": 1,
        "description": "New test",
        "type": 1,
        "control": 1,
        "date_start": date_start.strftime("%d.%m.%Y"),
        "date_end": date_end.strftime("%d.%m.%Y"),
    }
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 2,
        "name": "Another test task",
        "description": "New test",
        "idp": 1,
        "type": "Project",
        "status_progress": "in_work",
        "is_completed": False,
        "control": "Test",
        "date_start": date_start.strftime("%d.%m.%Y"),
        "date_end": date_end.strftime("%d.%m.%Y"),
        "comments": [],
    }

    client.force_login(Employee.objects.get(id=3))
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"error": "Вы не являетесь автором данного ИПР."}


@pytest.mark.django_db
def test_update_task_is_completed(
    client: APIClient,
    create_task,
):
    task = create_task
    # employees = create_employee
    client.force_login(Employee.objects.get(id=4))

    url = f"/api/tasks/{task.id}/"
    data = {"is_completed": True}

    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK

    # Перезагружаем объект из базы данных, чтобы получить актуальные данные
    task.refresh_from_db()
    # Проверяем, что данные были обновлены
    assert task.is_completed is True

    client.force_login(Employee.objects.get(id=1))
    data = {"status_progress": "in_work"}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    # Перезагружаем объект из базы данных, чтобы получить актуальные данные
    task.refresh_from_db()
    # Проверяем, что данные не были обновлены
    assert task.is_completed is False

    client.force_login(Employee.objects.get(id=2))
    data = {"status_progress": "done"}
    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    # Перезагружаем объект из базы данных, чтобы получить актуальные данные
    task.refresh_from_db()
    # Проверяем, что данные не были обновлены
    assert task.status_progress == "in_work"


@pytest.mark.django_db
def test_update_task_status_progress(client: APIClient, create_task, create_employee):
    task = create_task
    client.force_login(Employee.objects.get(id=4))

    url = f"/api/tasks/{task.id}/"
    data = {"status_progress": "done"}

    response = client.patch(url, data, content_type="application/json")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Перезагружаем объект из базы данных, чтобы получить актуальные данные
    task.refresh_from_db()
    # Проверяем, что данные были обновлены
    assert task.status_progress == "in_work"

    # client.force_login(Employee.objects.get(id=2))
    # data = {"status_progress": "done"}
    # response = client.patch(url, data, content_type="application/json")
    # assert response.status_code == status.HTTP_400_BAD_REQUEST
    # # Перезагружаем объект из базы данных, чтобы получить актуальные данные
    # task.refresh_from_db()
    # # Проверяем, что данные не были обновлены
    # assert task.status_progress == "done"


@pytest.mark.django_db
def test_delete_task(client: APIClient, create_task, create_employee):
    task = create_task
    client.force_login(Employee.objects.get(id=4))

    response = client.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    client.force_login(Employee.objects.get(id=1))
    response = client.delete(f"/api/tasks/{task.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
