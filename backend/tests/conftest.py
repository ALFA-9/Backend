import datetime as dt

import pytest

from idps.models import Employee, Idp


@pytest.fixture
def create_multiple_directors():
    for dir in range(1, 4):
        Employee.objects.create(
            first_name=f"Emp{dir}",
            email=f"email{dir}@dir.com",
            phone=f"7 (999) 99{dir}-00-00",
        )


@pytest.fixture
def create_employees_for_director_1(create_multiple_directors):
    for emp in range(1, 4):
        Employee.objects.create(
            first_name=f"Emp1-{emp}",
            email=f"email1-{emp}@dir.com",
            phone=f"7 (999) 991-{emp}0-00",
            director=Employee.objects.get(id=1),
        )


@pytest.fixture
def create_idp(create_employees_for_director_1):
    date_start = dt.date.today()
    date_end = date_start + dt.timedelta(days=180)
    return Idp.objects.create(
        title="Title",
        employee=Employee.objects.get(id=4),
        director=Employee.objects.get(id=1),
        status_idp="in_work",
        date_end=date_end,
    )
