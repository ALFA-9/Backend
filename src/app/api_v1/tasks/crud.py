from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Comment, Employee, Idp, Task
from app.utils import get_all_parents_id


async def post(db: AsyncSession, user: Employee, payload):
    statement = select(Idp).where(Idp.id == payload.idp_id)
    idp = await db.scalar(statement)
    if idp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IDP not found",
        )
    if idp.director_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisson denied",
        )
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
            detail="Task not found",
        )
    if task.idp.director_id != user.id or task.idp.employee_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisson denied",
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
            detail="Task not found",
        )
    if task.idp.director_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisson denied",
        )
    await db.delete(task)
    await db.commit()


async def post_comment(db: AsyncSession, user: Employee, id: int, payload):
    existing_model = await db.execute(select(Task).where(Task.id == id))
    task = existing_model.scalar()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    idp_emp = task.idp.employee_id
    directors_id = await db.execute(select(get_all_parents_id(idp_emp)))
    directors_id = directors_id.scalars().all()
    if user.id not in (directors_id + [idp_emp]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisson denied",
        )
    comment = Comment(
        task_id=id,
        employee_id=user.id,
        body_comment=payload.body_comment,
    )
    db.add(comment)
    await db.commit()
    return comment
