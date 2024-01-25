from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin, ModelView

from app.database.db import engine
from app.database.models import Base, Employee
from app.employees import routers


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
admin = Admin(app, engine)


class UserAdmin(ModelView, model=Employee):
    column_list = [Employee.id, Employee.email]


admin.add_view(UserAdmin)

# Добавляем маршруты как в Django
app.include_router(routers.router, prefix="/employees", tags=["employees"])
app.include_router(routers.router, prefix="/idps", tags=["idps"])
app.include_router(routers.router, prefix="/tasks", tags=["tasks"])
