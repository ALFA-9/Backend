from app.api import employees, grades
from app.db import database, engine, metadata
from fastapi import FastAPI
from contextlib import asynccontextmanager

metadata.create_all(engine)
app = FastAPI()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Before start
    await database.connect()
    yield
    # Before finish
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

# Добавляем маршруты как в Django
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(grades.router, prefix="/grades", tags=["grades"])
