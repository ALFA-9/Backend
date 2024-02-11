import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.models import (Base, Department, Employee, Grade, Post,
                                 TaskControl, TaskType)
from app.database.session import get_db
from app.main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    class_=AsyncSession,
)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session
        await session.close()


@pytest_asyncio.fixture()
async def session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def client():
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


@pytest_asyncio.fixture()
async def create_employees(session):
    async with TestingSessionLocal() as db:
        grades = [Grade(title=f"Grade{i}") for i in range(1, 6)]
        db.add_all(grades)
        posts = [Post(title=f"Post{i}") for i in range(1, 6)]
        db.add_all(posts)
        departments = [Department(title=f"Department{i}") for i in range(1, 6)]
        db.add_all(departments)
        type = TaskType(name="Project")
        db.add(type)
        control = TaskControl(title="Test")
        db.add(control)
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
                department=departments[0],
            )
            # Устанавливаем атрибут director для иерархической структуры
            if i > 1:
                employee.director = employee_list[i - 2]

            employee_list.append(employee)
        db.add_all(employee_list)
        await db.commit()
    await db.close()
