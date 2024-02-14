import datetime as dt

from celery import shared_task
from sqlalchemy import select

from app.database.models import Task
from app.database.session import get_db


@shared_task
async def update_status_for_task():
    """Обновлем статус для просроченных задач."""
    db = await get_db
    statement = select(Task).where(
        Task.status_progress == "in_work", Task.date_end < dt.date.today()
    )
    result = await db.execute(statement)
    tasks = result.unique().scalars().all()
    for task in tasks:
        task.statis_idp = "not_completed"
    await db.commit()
    await db.refresh(tasks)
    for i in tasks:
        print(i)
    return None
