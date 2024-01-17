from typing import List

from app.api import crud
from app.api.models import EmployeeDB
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get('/', response_model=List[EmployeeDB])
async def get_all_employees():
    return await crud.get_all_employees()


@router.get("/{id}/", response_model=EmployeeDB)
async def get_employee(id: int):
    employee = await crud.get_emplyee(id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
