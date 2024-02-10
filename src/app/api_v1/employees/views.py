from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.employees import crud
from app.api_v1.employees.schemas import (DirectorSchema, EmployeeChild,
                                          EmployeeSchema, EmployeeWithIdps)
from app.auth.auth import get_current_auth_user
from app.constants import EXAMPLE_EMPLOYEE_404
from app.database.models import Employee
from app.database.session import get_db

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=list[EmployeeSchema])
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.get_all(db, user)


@router.get("/me/", response_model=EmployeeWithIdps)
async def auth_user_check_self_info(
    user: Employee = Depends(get_current_auth_user),
):
    return user


@router.get("/subordinates/", response_model=list[EmployeeChild])
async def get_subordinates(
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.get_subordinates(db, user)


@router.get("/directors/", response_model=list[DirectorSchema])
async def get_directors(
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.get_directors(db, user)


@router.get(
    "/{id}/",
    response_model=EmployeeWithIdps,
    responses={
        404: EXAMPLE_EMPLOYEE_404,
    },
)
async def get_employee(
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    employee = await crud.get_by_id_with_joined(db, id, user)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )
    return employee
