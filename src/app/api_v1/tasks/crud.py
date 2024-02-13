from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.tasks.schemas import TaskPatch
from app.constants import SUBJECT
from app.database.models import Comment, Employee, Idp, Task
from app.utils import get_all_parents_id, send_email


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
            detail="Permission denied",
        )
    task = Task(
        name=payload.name,
        description=payload.description,
        idp_id=payload.idp_id,
        date_start=payload.date_start,
        date_end=payload.date_end,
        type_id=payload.type_id,
        control_id=payload.control_id,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def patch(
    db: AsyncSession,
    user: Employee,
    payload: TaskPatch,
    id: int,
    background_tasks: BackgroundTasks,
):
    existing_model = await db.execute(select(Task).where(Task.id == id))
    task = existing_model.scalar()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    if task.idp.director_id != user.id:
        payload.is_completed = False
        for field, value in payload:
            setattr(task, field, value)
        await db.commit()
        await db.refresh(task)
        if payload.status_progress:
            background_tasks.add_task(
                send_email,
                SUBJECT,
                f"Статус задачи {task.name} изменен на {payload.status_progress}.",
                task.idp.employee.id,
            )
        return task
    elif task.idp.employee_id == user.id:
        setattr(task, "is_completed", True)
        await db.commit()
        await db.refresh(task)
        return task
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Permission denied",
    )


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
            detail="Permission denied",
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
            detail="Permission denied",
        )
    comment = Comment(
        task_id=id,
        employee_id=user.id,
        body_comment=payload.body_comment,
    )
    db.add(comment)
    await db.commit()
    return comment
