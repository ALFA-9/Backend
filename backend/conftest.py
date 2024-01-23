import datetime as dt

import pytest

from idps.models import Employee, Idp


@pytest.fixture
def create_multiple_employees():
    models = [Employee.objects.create(name=f"Emp{i}") for i in range(1, 3)]
    return models


@pytest.fixture
def create_tree_structure():
    for dir in range(1, 4):
        director = Employee.objects.create(
            name=f"Emp{dir}", email=f"email{dir}@dir.com"
        )
        if dir == 1:
            for emp_dir in range(1, 3):
                emp_director = Employee.objects.create(
                    name=f"Emp{dir}-{emp_dir}",
                    email=f"email{dir}-{emp_dir}@dir.com",
                    director=director,
                )
                if emp_dir == 2:
                    Employee.objects.create(
                        name=f"Emp{dir}-{emp_dir}-1",
                        email=f"email{dir}-{emp_dir}-1@dir.com",
                        director=emp_director,
                    )
        else:
            for emp_dir in range(1, 3):
                Employee.objects.create(
                    name=f"Emp{dir}-{emp_dir}",
                    email=f"email{dir}-{emp_dir}@dir.com",
                    director=director,
                )


@pytest.fixture
def create_idps_for_emps(create_tree_structure):
    STATUSES = ["in_work", "canceled", "done"]
    for i in range(2, 5):
        emp = Employee.objects.get(id=i)
        Idp.objects.create(
            title=f"ИПР для {emp.name}",
            employee=emp,
            director=emp.director,
            date_end=dt.date.today() + dt.timedelta(days=180),
            status_idp=STATUSES[i - 2],
        )
    emp = Employee.objects.get(id=7)
    Idp.objects.create(
        title=f"ИПР для {emp.name}",
        employee=emp,
        director=emp.director,
        date_end=dt.date.today() + dt.timedelta(days=180),
        status_idp="not_completed",
    )


@pytest.fixture
def create_idp_model(create_multiple_employees):
    date_start = dt.date.today()
    date_end = date_start + dt.timedelta(days=180)
    return Idp.objects.create(
        title="Title",
        employee=create_multiple_employees[1],
        director=create_multiple_employees[0],
        status_idp="in_work",
        date_end=date_end,
    )
