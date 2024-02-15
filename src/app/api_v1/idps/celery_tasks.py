import asyncio
import datetime as dt

from sqlalchemy import func, select

from app.celery import celery_app
from app.database.models import Idp, Task
from app.database.session import SessionLocal


async def async_body():
    """Обновляем статус ИПР, если последняя задача просрочилась."""
    async with SessionLocal() as session:
        subquery = (
            select(Task.idp_id, func.max(Task.date_end).label("max_date_end"))
            .where(Task.is_completed is not True)
            .group_by(Task.idp_id)
            .subquery()
        )
        statement = (
            select(Idp)
            .join(subquery, Idp.id == subquery.c.idp_id)
            .filter(
                Idp.status_idp == "in_work",
                subquery.c.max_date_end < dt.date.today(),
            )
        )
        result = await session.execute(statement)
        idps = result.unique().scalars().all()
        for idp in idps:
            idp.status_idp = "not_completed"
        await session.commit()
        # for idp in idps:
        #     await session.refresh(idp)
        #     print(idp)


@celery_app.task
def update_status_for_idp():
    asyncio.run(async_body())
    return None
