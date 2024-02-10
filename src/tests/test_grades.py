import json

from app.api import crud


def test_create_grade(test_app, monkeypatch):
    test_request_payload = {"title": "something"}
    test_response_payload = {"id": 1, "title": "something"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post_grade", mock_post)

    response = test_app.post("/grades/", data=json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_grade_invalid_json(test_app):
    response = test_app.post("/grades/", data=json.dumps({"name": "something"}))
    assert response.status_code == 422


def test_read_grade(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "title": "something",
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get_grade", mock_get)

    response = test_app.get("/grades/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_grade_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get_grade", mock_get)

    response = test_app.get("/grades/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Grade not found"


def test_read_all_notes(test_app, monkeypatch):
    test_data = [
        {"title": "something", "id": 1},
        {"title": "someone", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all_grades", mock_get_all)

    response = test_app.get("/grades/")
    assert response.status_code == 200
    assert response.json() == test_data
