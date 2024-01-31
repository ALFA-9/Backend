import datetime as dt
from http import HTTPStatus

import pytest
from django.utils.translation import gettext_lazy as _
from rest_framework.test import APIClient

from users.models import Employee


@pytest.mark.django_db
def test_post_idp(client: APIClient, create_employees_for_director_1):
    client.force_login(Employee.objects.get(id=1))
    url = "/api/idps/"
    date_start = dt.date.today()
    date_end = date_start + dt.timedelta(days=180)
    data = {
        "title": "Title",
        "employee": 5,
        "status_idp": "in_work",
        "date_end": date_end.strftime("%d.%m.%Y"),
    }
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "title": "Title",
        "employee": 5,
        "director": 1,
        "status_idp": "in_work",
        "date_start": date_start.strftime("%d.%m.%Y"),
        "date_end": date_end.strftime("%d.%m.%Y"),
    }

    client.force_login(Employee.objects.get(id=2))
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "error": "Вы не являетесь начальником для этого сотрудника."
    }


@pytest.mark.django_db
def test_post_idp_when_emp_have_active(client: APIClient, create_idp):
    client.force_login(Employee.objects.get(id=1))
    url = "/api/idps/"
    date_start = dt.date.today()
    date_end = date_start + dt.timedelta(days=180)
    data = {
        "title": "Title2",
        "employee": 4,
        "status_idp": "in_work",
        "date_end": date_end.strftime("%d.%m.%Y"),
    }

    response = client.post(url, data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        "error": "У этого сотрудника уже есть активный ИПР."
    }


@pytest.mark.django_db
def test_post_incorrect_idp(
    client: APIClient, create_employees_for_director_1
):
    client.force_login(Employee.objects.get(id=1))
    date_start = dt.date.today()
    date_end = date_start - dt.timedelta(days=1)
    url = "/api/idps/"
    data = {
        "employee": 4,
        "status_idp": "uncorrect_type",
        "date_end": date_end,
    }
    response = client.post(url, data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    print(response.json())
    assert response.json() == {
        "title": [_("Обязательное поле.")],
        "date_end": ["Дата окончания должна быть больше даты начала."],
        "status_idp": [
            "Значения uncorrect_type нет среди допустимых вариантов."
        ],
    }


@pytest.mark.django_db
def test_api_endpoint(client: APIClient, create_idp):
    client.force_login(Employee.objects.get(id=1))
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
        assert "email" in element["employee"]

        assert "id" in element["director"]
        assert "email" in element["director"]


# @pytest.mark.django_db
# def test_statistic(client: APIClient, create_idps_for_emps):
#     url = "/api/statistic/"

#     response = client.get(url)
#     assert response.json() == {"in_work": 1, "canceled": 1, "done": 1}

#     response = client.patch(
#         "/api/idps/1/",
#         {"status_idp": "not_completed"},
#         format="Content-Type",
#         content_type="application/json",
#     )
#     assert response.status_code == 200

#     response = client.get(url)
#     assert response.json() == {"not_completed": 1, "canceled": 1, "done": 1}

#     data = {
#         "title": "Title",
#         "employee": 2,
#         "director": 1,
#         "status_idp": "in_work",
#         "date_end": "20.03.2024",
#     }
#     response = client.post("/api/idps/", data)
#     assert response.status_code == 201
#     response = client.get(url)
#     assert response.json() == {"in_work": 1, "canceled": 1, "done": 1}
