from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.models import Employee, Idp
from app.utils import get_all_childs_id, get_all_parents_id


async def get_all(
    db: AsyncSession,
    user: Employee,
):
    childs_id = get_all_childs_id(user.id)
    statement = (
        select(Employee).filter(Employee.id.in_(select(childs_id))).order_by("id")
    )
    childs = await db.execute(statement)
    return childs.unique().scalars().all()


async def get_subordinates(
    db: AsyncSession,
    user: Employee,
):
    statement = (
        select(Employee).options(
            joinedload(Employee.employees).options(
                joinedload(Employee.employees).options(
                    joinedload(Employee.employees).options(
                        joinedload(Employee.employees)
                    )
                )
            ),
        )
    ).where(Employee.director_id == user.id)
    result = await db.execute(statement)
    return result.unique().scalars().all()


async def get_directors(
    db: AsyncSession,
    user: Employee,
):
    directors_id = get_all_parents_id(user.id)
    statement = select(Employee).filter(Employee.id.in_(select(directors_id)))
    result = await db.execute(statement)
    return result.unique().scalars().all()


async def get_by_id_with_joined(db: AsyncSession, id: int, user: Employee):
    childs_id = get_all_childs_id(user.id)
    statement = (
        select(Employee)
        .options(joinedload(Employee.idp_emp).options(joinedload(Idp.director)))
        .filter(Employee.id.in_(select(childs_id)))
        .where(Employee.id == id)
    )
    result = await db.execute(statement)
    return result.unique().scalar()