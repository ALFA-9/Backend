from app.database.models import Idp
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload


# Получаем ответ от дб
async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100):
    statement = select(Idp).options(
        joinedload(Idp.employee),
        joinedload(Idp.director),
        joinedload(Idp.status_idp),
    ).offset(skip).limit(limit)
    result = await db.execute(statement)
    return result.unique().scalars().all()


async def get_by_id(db: AsyncSession, id: int):
    return db.query(Idp).first()
