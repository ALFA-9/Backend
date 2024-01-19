from app.db import database, Employee
from sqlalchemy.orm import Session


# Получаем ответ от дб
def get_all_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).offset(skip).limit(limit).all()


async def get_employee(id: int):
    query = Employee.select().where(id == Employee.id)
    return await database.fetch_one(query=query)
