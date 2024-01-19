from app.api import grades
from app.db import engine, Base, SessionLocal
from fastapi import FastAPI

from app.api.employees import employees

Base.metadata.create_all(engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Добавляем маршруты как в Django
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(grades.router, prefix="/grades", tags=["grades"])
