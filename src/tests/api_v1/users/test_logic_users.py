import pytest
from fastapi import status
# from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_auth(client, create_employees):
    url = "/auth/login/"
    data = {"email": "ivan.ivanov2@example.com"}
    response = client.post(url, json=data)
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert response.json().get("access_token")


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[2]], indirect=True)
async def test_user_employees(client, create_employees, get_token):
    url = "/api/v1/employees/"
    response = client.get(url, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[2]], indirect=True)
async def test_user_directors(client, create_employees, get_token):
    url = "/api/v1/employees/directors/"
    response = client.get(url, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[2]], indirect=True)
async def test_user_subordinates(client, create_employees, get_token):
    url = "/api/v1/employees/subordinates/"
    response = client.get(url, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert isinstance(response.json()[0]["employees"], list)


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[2]], indirect=True)
async def test_user_me(client, create_employees, get_token):
    url = "/api/v1/employees/me/"
    response = client.get(url, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 2,
        "director": 1,
        "first_name": "Иван2",
        "last_name": "Иванов2",
        "patronymic": "Иванович2",
        "post": "Post2",
        "idps": [],
        "department": "Department1",
        "grade": "Grade2"
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("get_token", [[2]], indirect=True)
async def test_employee_by_id(client, create_employees, get_token):
    url = "/api/v1/employees/3/"
    response = client.get(url, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 3,
        "director": 2,
        "first_name": "Иван3",
        "last_name": "Иванов3",
        "patronymic": "Иванович3",
        "post": "Post3",
        "idps": [],
        "department": "Department1",
        "grade": "Grade3"
    }

    url = "/api/v1/employees/1/"
    response = client.get(url, headers={"Authorization": get_token[0]})
    assert response.status_code == status.HTTP_404_NOT_FOUND
