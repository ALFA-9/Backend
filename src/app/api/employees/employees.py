from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.employees import crud
from app.api.employees.models import EmployeeDB
from app.database.db import get_db

router = APIRouter()


@router.get("/", response_model=list[EmployeeDB])
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)


@router.get("/{id}/", response_model=EmployeeDB)
async def get_employee(id: int, db: AsyncSession = Depends(get_db)):
    employee = await crud.get_by_id(db, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
