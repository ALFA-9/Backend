from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from app.admin import init
from app.auth.auth import router as auth_router
from app.database.models import Base
from app.database.session import engine
from app.employees.views import router as router_employees
from app.idps.views import router as router_idps
from app.tasks.views import router as router_tasks


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
app.include_router(router_employees)
app.include_router(router_idps)
app.include_router(router_tasks)
