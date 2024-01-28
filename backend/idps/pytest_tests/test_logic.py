# import datetime as dt
# from http import HTTPStatus

# import pytest
# from rest_framework.test import APIClient


# @pytest.mark.django_db
# def test_api_endpoint(client: APIClient, create_idp_model):
#     url = "/api/idps/"

#     response = client.get(url)
#     assert response.status_code == HTTPStatus.OK
#     assert isinstance(response.json(), list)
#     for element in response.json():
#         assert "title" in element
#         assert "employee" in element
#         assert "director" in element
#         assert "status_idp" in element
#         assert "date_start" in element
#         assert "date_end" in element

#         assert "id" in element["employee"]
#         assert "name" in element["employee"]

#         assert "id" in element["director"]
#         assert "name" in element["director"]


# @pytest.mark.django_db
# def test_post_idp_response(client: APIClient, create_multiple_employees):
#     url = "/api/idps/"
#     date_start = dt.date.today()
#     date_end = date_start + dt.timedelta(days=180)
#     data = {
#         "title": "Title",
#         "employee": 2,
#         "director": 1,
#         "status_idp": "in_work",
#         "date_end": date_end.strftime("%d.%m.%Y"),
#     }
#     response = client.post(url, data)
#     assert response.status_code == HTTPStatus.CREATED
#     assert response.json() == {
#         "id": 1,
#         "title": "Title",
#         "employee": 2,
#         "director": 1,
#         "status_idp": "in_work",
#         "date_start": date_start.strftime("%d.%m.%Y"),
#         "date_end": date_end.strftime("%d.%m.%Y"),
#     }


# @pytest.mark.django_db
# def test_post_incorrect_idp(client: APIClient, create_idp_model):
#     url = "/api/idps/"
#     data = {
#         "title": "Title",
#         "employee": 2,
#         "status_idp": "in_work",
#         "date_end": "20.03.2024",
#     }
#     response = client.post(url, data)
#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json() in (
#         {"director": ["Обязательное поле."]},
#         {"director": ["Required field."]},
#     )

#     data["director"] = 1
#     data["status_idp"] = "uncorrect_type"
#     response = client.post(url, data)
#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json() == {
#         "status_idp": [
#             "Значения uncorrect_type нет среди допустимых вариантов."
#         ]
#     }


# @pytest.mark.django_db
# def test_post_exists_idp(client: APIClient, create_idp_model):
#     url = "/api/idps/"
#     data = {
#         "title": "Title",
#         "employee": 2,
#         "director": 1,
#         "status_idp": "in_work",
#         "date_end": "20.03.2024",
#     }

#     response = client.post(url, data)
#     assert response.status_code == HTTPStatus.BAD_REQUEST


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
