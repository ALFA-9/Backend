import asyncio
import datetime as dt

from sqlalchemy import select

from app.celery import celery_app
from app.database.models import Task
from app.database.session import SessionLocal


async def async_body():
    """Обновлем статус для просроченных задач."""
    async with SessionLocal() as session:
        statement = select(Task).where(
            Task.status_progress == "in_work",
            Task.date_end < dt.date.today(),
            Task.is_completed is not True,
        )
        result = await session.execute(statement)
        tasks = result.unique().scalars().all()
        for task in tasks:
            task.status_progress = "not_completed"
        await session.commit()
        # for task in tasks:
        #     await session.refresh(task)
        #     print(task)


@celery_app.task
def update_status_for_task():
    """Обновлем статус для просроченных задач."""
    asyncio.run(async_body())
    return None
