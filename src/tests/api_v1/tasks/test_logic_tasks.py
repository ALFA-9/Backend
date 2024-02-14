from datetime import datetime, timedelta

import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[1, 3]], indirect=True)
async def test_post_task(client: TestClient, get_token, create_idp):
    url = "/api/v1/tasks/"
    date_start = datetime.utcnow()
    date_end = date_start + timedelta(days=180)

    data = {
        "name": "Another test task",
        "idp": 1,
        "description": "New test",
        "type": 1,
        "control": 1,
        "date_start": date_start.strftime("%d.%m.%Y"),
        "date_end": date_end.strftime("%d.%m.%Y"),
    }
    response = client.post(url, json=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_201_CREATED
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
    }

    response = client.post(url, json=data, headers={"Authorization": get_token[1]})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Permission denied"}


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[4, 1, 2]], indirect=True)
async def test_update_task_is_completed(
    client: TestClient,
    get_token,
    create_idp,
):
    date_start = datetime.utcnow()
    date_end = date_start + timedelta(days=180)

    url = "/api/v1/tasks/1/"
    data = {"is_completed": True}

    response = client.patch(url, json=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "Test task",
        "description": "New test",
        "idp": 1,
        "type": "Project",
        "status_progress": "in_work",
        "is_completed": True,
        "control": "Test",
        "date_start": date_start.strftime("%d.%m.%Y"),
        "date_end": date_end.strftime("%d.%m.%Y"),
    }

    data = {"status_progress": "done"}
    response = client.patch(url, json=data, headers={"Authorization": get_token[1]})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "Test task",
        "description": "New test",
        "idp": 1,
        "type": "Project",
        "status_progress": "done",
        "is_completed": False,
        "control": "Test",
        "date_start": date_start.strftime("%d.%m.%Y"),
        "date_end": date_end.strftime("%d.%m.%Y"),
    }

    data = {"status_progress": "in_work"}
    response = client.patch(url, json=data, headers={"Authorization": get_token[2]})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Permission denied"}


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[4]], indirect=True)
async def test_update_task_status_progress(client: TestClient, get_token, create_idp):
    url = "/api/v1/tasks/1/"
    data = {"status_progress": "done"}

    response = client.patch(url, json=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"detail": "Permission denied"}


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[3, 1]], indirect=True)
async def test_delete_task(client: TestClient, get_token, create_idp):
    url = "/api/v1/tasks/1/"

    response = client.delete(url, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.delete(url, headers={"Authorization": get_token[1]})
    assert response.status_code == status.HTTP_204_NO_CONTENT
