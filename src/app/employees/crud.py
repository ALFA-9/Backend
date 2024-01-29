from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.models import Employee
from app.utils import get_all_childs_id


# Получаем ответ от дб
async def get_all(
    db: AsyncSession,
    user: Employee,
):
    statement = (
        select(Employee).options(
            joinedload(Employee.grade),
            joinedload(Employee.employees).options(
                joinedload(Employee.employees)
            ),
        )
    ).where(Employee.id == user.id)
    result = await db.execute(statement)
    return result.unique().scalars().all()


async def get_by_email(db: AsyncSession, email: str):
    statement = select(Employee).where(Employee.email == email)
    result = await db.execute(statement)
    return result.scalars().first()


async def get_by_id_with_joined(db: AsyncSession, id: int, user: Employee):
    childs_id = get_all_childs_id(user.id)
    statement = (
        select(Employee)
        .filter(Employee.id.in_(select(childs_id)))
        .where(Employee.id == id)
    )
    employees = await db.execute(statement)
    return employees.unique().scalar()
