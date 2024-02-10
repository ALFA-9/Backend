from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.models import Employee, Idp


async def get_by_email(db: AsyncSession, email: str):
    statement = (
        select(Employee)
        .options(joinedload(Employee.idp_emp).options(joinedload(Idp.director)))
        .where(Employee.email == email)
    )
    result = await db.execute(statement)
    return result.scalars().first()
