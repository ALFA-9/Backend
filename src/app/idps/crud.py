from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.models import Comment, Employee, Idp, Task
from app.utils import get_all_childs_id, get_all_parents_id, send_email


async def director_permission(
    db: AsyncSession, user: Employee, employee_id: int
):
    childs_id = await db.execute(select(get_all_childs_id(user.id)))
    if employee_id not in childs_id.scalars().all():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете взаимодействовать с данным сотрудником.",
        )


async def get_all(
    db: AsyncSession, user: Employee, skip: int = 0, limit: int = 100
):
    statement = (
        select(Idp)
        .options(
            joinedload(Idp.employee),
            joinedload(Idp.director),
        )
        .offset(skip)
        .limit(limit)
    ).where(Idp.employee_id == user.id)
    result = await db.execute(statement)
    return result.unique().scalars().all()


async def get_by_id(db: AsyncSession, user: Employee, id: int):
    statement = (
        select(Idp)
        .options(
            joinedload(Idp.tasks).options(
                joinedload(Task.comment).options(joinedload(Comment.employee))
            )
        )
        .where(
            Idp.id == id,
            or_(Idp.director_id == user.id, Idp.employee_id == user.id),
        )
    )
    return await db.scalar(statement)


async def post(db: AsyncSession, user: Employee, payload):
    await director_permission(db, user, payload.employee_id)
    active_idps = await db.execute(
        select(Idp).where(
            Idp.status_idp == "in_work", Idp.employee_id == payload.employee_id
        )
    )
    active_idps = active_idps.unique().scalars().all()
    if len(active_idps) == 0:
        idp = Idp(
            title=payload.title,
            employee_id=payload.employee_id,
            director_id=user.id,
            date_end=payload.date_end,
        )
        db.add(idp)
        await db.flush()
        for task_data in payload.tasks:
            task = Task(
                name=task_data.name,
                description=task_data.description,
                idp_id=idp.id,
                date_start=task_data.date_start,
                date_end=task_data.date_end,
                type_id=task_data.type_id,
                control_id=task_data.control_id,
            )
            db.add(task)
        await db.commit()
        await db.refresh(idp)
        return idp
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="У этого сотрудника уже есть активный ИПР.",
    )


async def patch(db: AsyncSession, user: Employee, payload, id: int):
    existing_model = await db.execute(select(Idp).where(Idp.id == id))
    idp = existing_model.scalar()
    if not idp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ИПР с таким id не существует",
        )
    await director_permission(db, user, idp.employee_id)
    for field, value in payload:
        setattr(idp, field, value)
    await db.commit()
    return idp


async def post_request(db: AsyncSession, user: Employee, payload):
    directors_id = get_all_parents_id(user.id)
    statement = (
        select(Employee)
        .filter(Employee.id.in_(select(directors_id)))
        .where(Employee.id == payload.director_id)
    )
    result = await db.execute(statement)
    if (director := result.scalar()) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Это не ваш начальник.",
        )
    try:
        await send_email(
            payload.title, payload.letter, payload.files, director.email,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Мы не смогли отправить сообщение.",
        )
    return payload