from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.db import engine
from app.database.models import Base
from app.employees import routers


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


# Добавляем маршруты как в Django
app.include_router(routers.router, prefix="/employees", tags=["employees"])
app.include_router(routers.router, prefix="/idps", tags=["idps"])
