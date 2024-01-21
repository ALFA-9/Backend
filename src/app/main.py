from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.employees import employees
from app.database.db import engine
from app.database.models import Base


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


# Добавляем маршруты как в Django
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(employees.router, prefix="/idps", tags=["idps"])
