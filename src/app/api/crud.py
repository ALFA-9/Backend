from app.api.models import GradeSchema
from app.db import Grade
from sqlalchemy.orm import Session


# Получаем ответ от дб
def get_all_grades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Grade).offset(skip).limit(limit).all()


async def get_grade(db: Session, id: int):
    return await db.query(Grade).filter(Grade.id == id).first()


async def post_grade(db: Session, payload: GradeSchema):
    query = Grade.insert().values(title=payload.title)
    return await db.execute(query=query)
