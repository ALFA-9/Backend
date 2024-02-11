import pytest

from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_user_auth(client: AsyncClient, create_employees):
    url = "/auth/login/"
    data = {"email": "ivan.ivanov2@example.com"}
    response = await client.post(url, json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("access_token")
