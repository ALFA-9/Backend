from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.models import Task


# Получаем ответ от дб
async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100):
    statement = select(Task).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.unique().scalars().all()


async def get_by_id(db: AsyncSession, id: int):
    statement = select(Task).where(Task.id == id)
    return await db.scalar(statement)


async def post(db: AsyncSession, payload):
    task = Task(
        name=payload.name,
        description=payload.description,
        idp_id=payload.idp_id,
        date_start=payload.date_start,
        date_end=payload.date_end,
    )
    db.add(task)
    await db.commit()
    return task
