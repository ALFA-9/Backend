import pytest

from idps.models import Employee, Idp


@pytest.fixture
def create_multiple_employees():
    models = [Employee.objects.create(name=f"Emp{i}") for i in range(1, 3)]
    return models


@pytest.fixture
def create_idp_model(create_multiple_employees):
    return Idp.objects.create(
        title="Title",
        employee=create_multiple_employees[1],
        director=create_multiple_employees[0],
        status_idp="in_work",
        date_start="2024-01-20",
        date_end="2024-03-20",
    )
