from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from app.admin import init
from app.api_v1 import router as api_v1_router
from app.auth.auth import router as auth_router
from app.database.models import Base
from app.database.session import engine


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(_: FastAPI):
    admin_backend = Admin(app, engine)
    init(admin_backend)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(api_v1_router)
