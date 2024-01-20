from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_api_endpoint(client: APIClient, create_idp_model):
    url = "/api/idps/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json(), list)
    for element in response.json():
        assert "title" in element
        assert "employee" in element
        assert "director" in element
        assert "status_idp" in element
        assert "date_start" in element
        assert "date_end" in element

        assert "id" in element["employee"]
        assert "name" in element["employee"]

        assert "id" in element["director"]
        assert "name" in element["director"]


@pytest.mark.django_db
def test_post_idp_response(client: APIClient, create_multiple_employees):
    url = "/api/idps/"
    data = {
        "title": "Title",
        "employee": 2,
        "director": 1,
        "status_idp": "in_work",
        "date_start": "2024-01-20",
        "date_end": "2024-03-20",
    }
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "title": "Title",
        "employee": 2,
        "director": 1,
        "status_idp": "in_work",
        "date_start": "2024-01-20",
        "date_end": "2024-03-20",
    }


@pytest.mark.django_db
def test_post_incorrect_idp(client: APIClient, create_idp_model):
    url = "/api/idps/"
    data = {
        "title": "Title",
        "employee": 2,
        "status_idp": "in_work",
        "date_start": "2024-01-20",
        "date_end": "2024-03-20",
    }
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() in (
        {"director": ["Обязательное поле."]},
        {"director": ["Required field."]},
    )

    data["director"] = 1
    data["status_idp"] = "uncorrect_type"
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "status_idp": [
            "Значения uncorrect_type нет среди допустимых вариантов."
        ]
    }


@pytest.mark.django_db
def test_post_exists_idp(client: APIClient, create_idp_model):
    url = "/api/idps/"
    data = {
        "title": "Title",
        "employee": 2,
        "director": 1,
        "status_idp": "in_work",
        "date_start": "2024-01-20",
        "date_end": "2024-03-20",
    }

    response = client.post(url, data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
