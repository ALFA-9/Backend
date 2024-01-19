from typing import List

from app.api.employees import crud
from app.api.employees.models import EmployeeDB
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get('/', response_model=List[EmployeeDB])
async def get_all_employees():
    return await crud.get_all_employees()


@router.get("/{id}/", response_model=EmployeeDB)
async def get_employee(id: int):
    employee = await crud.get_employee(id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
