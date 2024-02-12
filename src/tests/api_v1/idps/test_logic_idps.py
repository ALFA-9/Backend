from datetime import datetime, timedelta

import pytest
from fastapi import status
# from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[1, 4]], indirect=True)
async def test_post_idp(client, create_idp, get_token):
    url = "/api/v1/idps/"
    date_start = datetime.utcnow()
    date_end = date_start + timedelta(days=180)
    data = {
        "title": "Title",
        "employee_id": 2,
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
    response = client.post(url, json=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_201_CREATED
    print(response.json())
    assert response.json() == {
        "id": 2,
        "title": "Title",
        "employee_id": 2,
        "status_idp": "in_work",
        "tasks": [
            {
                "id": 2,
                "name": "Task",
                "description": "First task",
                "date_start": date_start.strftime("%d.%m.%Y"),
                "date_end": date_end.strftime("%d.%m.%Y"),
                "type": "Project",
                "control": "Test",
                "status_progress": "in_work",
                "is_completed": False,
            }
        ],
    }

    response = client.post(url, json=data, headers={"Authorization": get_token[1]})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[1]], indirect=True)
async def test_patch_idp(client, create_idp, get_token):
    url = "/api/v1/idps/1/"
    data = {
        "status_idp": "done",
    }

    response = client.patch(url, json=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[2]], indirect=True)
async def test_incorrect_user_patch_idp(client, create_idp, get_token):
    url = "/api/v1/idps/1/"
    data = {
        "status_idp": "done",
    }

    response = client.patch(url, json=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[1]], indirect=True)
async def test_post_idp_when_emp_have_active(client, create_idp, get_token):
    url = "/api/v1/idps/"
    date_start = datetime.utcnow()
    date_end = date_start + timedelta(days=180)
    data = {
        "title": "Title",
        "employee_id": 4,
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

    response = client.post(url, json=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[1]], indirect=True)
async def test_post_incorrect_idp(
    client,
    create_employees,
    get_token,
):
    date_start = datetime.utcnow()
    date_end = date_start - timedelta(days=1)
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
    response = client.post(url, json=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data.pop("title")
    data["tasks"][0]["date_start"] = date_end.strftime("%d.%m.%Y")
    response = client.post(url, json=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[4]], indirect=True)
async def test_api_endpoint(client, create_idp, get_token):
    url = "/api/v1/idps/"

    response = client.get(url, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_200_OK
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


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[2]], indirect=True)
async def test_idp_request(client, create_employees, get_token):
    url = "/api/v1/idps/request/"
    data = {
        "title": "New IDP",
        "letter": "I need it",
        "director_id": 1,
    }

    response = client.post(url, data=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "title": "New IDP",
        "letter": "I need it",
        "director_id": 1,
        "file": None,
    }

    response = client.post(url, data=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[4]], indirect=True)
async def test_idp_request_with_active_idp(client, create_idp, get_token):
    url = "/api/v1/idps/request/"
    data = {
        "title": "New IDP",
        "letter": "I need it",
        "director_id": 1,
    }

    response = client.post(url, data=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[2]], indirect=True)
async def test_idp_request_incorrect_director(client, create_employees, get_token):
    url = "/api/v1/idps/request/"
    data = {
        "title": "New IDP",
        "letter": "I need it",
        "director_id": 3,
    }

    response = client.post(url, data=data, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_403_FORBIDDEN
