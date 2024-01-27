from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.employees import crud
from app.employees.schemas import EmployeeDB
from app.auth.auth import get_current_auth_user

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=list[EmployeeDB])
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)


@router.get("/me/", response_model=EmployeeDB)
async def auth_user_check_self_info(
    user: EmployeeDB = Depends(get_current_auth_user),
):
    return user


@router.get("/{id}/", response_model=EmployeeDB)
async def get_employee(id: int, db: AsyncSession = Depends(get_db)):
    employee = await crud.get_by_id_with_joined(db, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
