from app.database.models import Employee
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload


# Получаем ответ от дб
async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100):
    statement = select(Employee).options(
        joinedload(Employee.grade),
        joinedload(Employee.employees).options(joinedload(Employee.employees)),
    ).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.unique().scalars().all()


async def get_by_id(db: AsyncSession, id: int):
    statement = select(Employee).options(
        joinedload(Employee.grade),
        joinedload(Employee.employees).options(joinedload(Employee.employees)),
    ).where(Employee.id == id)
    result = await db.execute(statement)
    return result.scalars().first()
