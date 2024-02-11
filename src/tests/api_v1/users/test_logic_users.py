import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest_asyncio.fixture()
async def get_token(client: AsyncClient, create_employees):
    url = "/auth/login/"
    data = {"email": "ivan.ivanov2@example.com"}
    response = await client.post(url, json=data)
    assert response.status_code == status.HTTP_200_OK
    return f'Bearer {response.json()["access_token"]}'


@pytest.mark.asyncio
async def test_user_auth(client: AsyncClient, create_employees):
    url = "/auth/login/"
    data = {"email": "ivan.ivanov2@example.com"}
    response = await client.post(url, json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("access_token")


@pytest.mark.asyncio
async def test_user_employees(client: AsyncClient, create_employees, get_token):
    url = "/api/v1/employees/"
    response = await client.get(url, headers={"Authorization": get_token})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_user_directors(client: AsyncClient, create_employees, get_token):
    url = "/api/v1/employees/directors/"
    response = await client.get(url, headers={"Authorization": get_token})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_user_subordinates(client: AsyncClient, create_employees, get_token):
    url = "/api/v1/employees/subordinates/"
    response = await client.get(url, headers={"Authorization": get_token})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert isinstance(response.json()[0]["employees"], list)


@pytest.mark.asyncio
async def test_user_me(client: AsyncClient, create_employees, get_token):
    url = "/api/v1/employees/me/"
    response = await client.get(url, headers={"Authorization": get_token})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}
