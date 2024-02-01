from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Employee, Idp, Task
from app.utils import get_all_childs_id


# Получаем ответ от дб
async def get_all(db: AsyncSession, user: Employee):
    statement = select(Task).where(Task.idp.employee_id == user.id)
    result = await db.execute(statement)
    return result.unique().scalars().all()


async def get_by_id(db: AsyncSession, user: Employee, id: int):
    statement = (
        select(Task)
        .join(Idp)
        .where(
            and_(
                Task.id == id,
                Idp.employee_id.in_(select(get_all_childs_id(user.id))),
            )
        )
    )
    result = await db.scalar(statement)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас недостаточно прав или такого id не существует.",
        )
    return result


async def post(db: AsyncSession, user: Employee, payload):
    statement = select(Idp).where(Idp.id == payload.idp_id)
    idp = await db.scalar(statement)
    if idp is None:
        raise HTTPException(
            status_code=status.HTTP_404_FORBIDDEN,
            detail="ИПР с таким id не существует.",
        )
    if idp.director_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас недостаточно прав.",
        )
    print(Task.StatusProgress.in_work)
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


async def patch(db: AsyncSession, user: Employee, payload, id: int):
    existing_model = await db.execute(select(Task).where(Task.id == id))
    task = existing_model.scalar()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задачи с таким id не существует",
        )
    if task.idp.director_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас недостаточно прав",
        )
    for field, value in payload:
        setattr(task, field, value)
    await db.commit()
    return task


async def delete(db: AsyncSession, user: Employee, id: int):
    existing_model = await db.execute(select(Task).where(Task.id == id))
    task = existing_model.scalar()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задачи с таким id не существует",
        )
    if task.idp.director_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас недостаточно прав",
        )
    await db.delete(task)
    await db.commit()
