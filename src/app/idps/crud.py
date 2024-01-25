from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.models import Idp


# Получаем ответ от дб
async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100):
    statement = (
        select(Idp)
        .options(
            joinedload(Idp.employee),
            joinedload(Idp.director),
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(statement)
    return result.unique().scalars().all()


async def get_by_id(db: AsyncSession, id: int):
    statement = (
        select(Idp)
        .options(joinedload(Idp.employee), joinedload(Idp.director))
        .where(Idp.id == id)
    )
    return await db.scalar(statement)


async def post(db: AsyncSession, payload):
    idp = Idp(
        title=payload.title,
        employee_id=payload.employee_id,
        director_id=payload.director_id,
        date_end=payload.date_end,
    )
    db.add(idp)
    await db.commit()
    return idp
