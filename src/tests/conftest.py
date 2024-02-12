from datetime import datetime, timedelta
import asyncio

from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings
from app.database.models import (Base, Department, Employee, Grade, Post,
                                 TaskControl, TaskType, Idp, Task)
from app.database.session import get_db
from app.main import app

test_db = factories.postgresql_noproc(
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    dbname="test_db",
)

TestingSessionLocal = async_sessionmaker()


@pytest.fixture(scope="session", autouse=True)
def connection_test(test_db):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password
    with DatabaseJanitor(pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password):
        engine = create_async_engine(f"postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}")
        TestingSessionLocal.configure(bind=engine)
        yield engine
        # await engine.dispose()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_tables(connection_test, test_db):
    engine = connection_test
    async with engine.connect() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        await connection.commit()


@pytest_asyncio.fixture()
async def get_app(connection_test):
    async def get_db_override():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override
    return app


@pytest.fixture()
def client(get_app):
    with TestClient(get_app) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def create_employees(create_tables):
    async with TestingSessionLocal() as db:
        grades = [Grade(title=f"Grade{i}") for i in range(1, 6)]
        db.add_all(grades)
        posts = [Post(title=f"Post{i}") for i in range(1, 6)]
        db.add_all(posts)
        department = Department(title="Department1")
        db.add(department)
        employee_list = []
        for i in range(1, 6):
            employee = Employee(
                first_name=f"Иван{i}",
                last_name=f"Иванов{i}",
                patronymic=f"Иванович{i}",
                email=f"ivan.ivanov{i}@example.com",
                phone=f"7 (917) 123-45-6{i}",
                grade=grades[i - 1],
                post=posts[i - 1],
                department=department,
            )
            # Устанавливаем атрибут director для иерархической структуры
            if i > 1:
                employee.director = employee_list[i - 2]

            employee_list.append(employee)
        db.add_all(employee_list)
        await db.commit()
        await db.close()
    return employee_list


@pytest_asyncio.fixture(scope="function")
async def get_token(client, create_employees, request):
    ids = request.param
    url = "/auth/login/"
    tokens = []
    for id in ids:
        data = {"email": f"ivan.ivanov{id}@example.com"}
        response = client.post(url, json=data)
        tokens.append(f'Bearer {response.json()["access_token"]}')
    return tokens


@pytest_asyncio.fixture(scope="function")
async def create_idp(create_employees):
    async with TestingSessionLocal() as db:
        date_start = datetime.utcnow()
        date_end = date_start + timedelta(days=180)
        employees = create_employees
        employee = employees[3]
        director = employees[0]
        type = TaskType(name="Project")
        db.add(type)
        control = TaskControl(title="Test")
        db.add(control)
        idp = Idp(
            title="Test idp",
            employee=employee,
            director=director,
            status_idp="in_work",
        )
        db.add(idp)
        task = Task(
            name="Test task",
            idp=idp,
            description="New test",
            task_type=type,
            task_control=control,
            date_start=date_start,
            date_end=date_end,
        )
        db.add(task)
        await db.commit()
        await db.close()
