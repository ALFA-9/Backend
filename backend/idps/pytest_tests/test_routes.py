# from http import HTTPStatus

# import pytest
# from rest_framework.test import APIClient


# @pytest.mark.django_db
# def test_api_endpoint(client: APIClient):
#     response = client.get("/api/idps/")
#     assert response.status_code == HTTPStatus.OK


# @pytest.mark.django_db
# def test_idp_by_id(client: APIClient, create_idp_model):
#     response = client.get("/api/idps/1/")
#     assert response.status_code == HTTPStatus.OK


# @pytest.mark.django_db
# def test_idp_by_not_exists_id(client: APIClient, create_idp_model):
#     response = client.get("/api/idps/2/")
#     assert response.status_code == HTTPStatus.NOT_FOUND


# @pytest.mark.django_db
# def test_statistic_exists(client: APIClient, create_idps_for_emps):
#     response = client.get("/api/statistic/")
#     assert response.status_code == HTTPStatus.OK
