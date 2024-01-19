from app.db import database, employees


# Получаем ответ от дб
async def get_all_employees():
    query = employees.select()
    return await database.fetch_all(query=query)


async def get_employee(id: int):
    query = employees.select().where(id == employees.c.id)
    return await database.fetch_one(query=query)
