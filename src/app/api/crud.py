from app.api.models import GradeSchema
from app.db import database, grades


# Получаем ответ от дб
async def get_all_grades():
    query = grades.select()
    return await database.fetch_all(query=query)


async def get_grade(id: int):
    query = grades.select().where(id == grades.c.id)
    return await database.fetch_one(query=query)


async def post_grade(payload: GradeSchema):
    query = grades.insert().values(title=payload.title)
    return await database.execute(query=query)
