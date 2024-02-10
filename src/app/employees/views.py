from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import get_current_token_payload
from app.database.models import Employee
from app.database.session import get_db
from app.employees import crud
from app.employees.schemas import (DirectorSchema, EmployeeChild,
                                   EmployeeSchema, EmployeeWithIdps)

router = APIRouter(prefix="/employees", tags=["employees"])


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(get_db),
) -> EmployeeChild:
    user_email: str | None = payload.get("sub")
    if user := await crud.get_by_email(db, user_email):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


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


@router.get("/{id}/", response_model=EmployeeWithIdps)
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
