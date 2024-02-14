import datetime as dt

from celery import shared_task
from sqlalchemy import func, select

from app.database.models import Idp, Task
from app.database.session import get_db


@shared_task
async def update_status_for_idp():
    """Обновляем статус ИПР, если последняя задача просрочилась."""
    db = await get_db()
    subquery = select(
        Task.idp_id, func.max(Task.date_end).label("max_date_end")
    ).group_by(Task.idp_id)
    statement = subquery.union_all(
        select(Idp)
        .where(Idp.id == subquery.c.idp_id)
        .filter(Idp.status_idp == "in_work", subquery.c.max_date_end < dt.date.today())
    )
    result = await db.execute(statement)
    idps = result.unique().scalars().all()
    for idp in idps:
        idp.status_idp = "not_completed"
    await db.commit()
    await db.refresh(idps)
    for i in idps:
        print(i)
    return None
