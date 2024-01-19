from typing import List

from app.db import SessionLocal
from app.api.employees import crud
from app.api.employees.models import EmployeeDB
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/', response_model=List[EmployeeDB])
def get_all_grades(db: Session = Depends(get_db)):
    return crud.get_all_employees(db)


@router.get("/{id}/", response_model=EmployeeDB)
async def get_employee(id: int):
    employee = await crud.get_employee(id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
