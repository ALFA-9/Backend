from app.database.db import get_db
from app.api.employees import crud
from app.api.employees.models import EmployeeDB
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/', response_model=list[EmployeeDB])
async def get_all_grades(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)


@router.get("/{id}/", response_model=EmployeeDB)
async def get_employee(id: int, db: AsyncSession = Depends(get_db)):
    employee = await crud.get_by_id(db, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
