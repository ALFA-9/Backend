from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.database.models import Employee
from app.employees.views import get_current_auth_user
from app.tasks import crud
from app.tasks.schemas import TaskCreate, TaskCreateDB, TaskDB, TaskPut

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskDB])
async def get_all_tasks(
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.get_all(db, user)


@router.get("/{id}/", response_model=TaskDB)
async def get_task(
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    idp = await crud.get_by_id(db, user, id)
    if not idp:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return idp


@router.post("/", response_model=TaskCreateDB)
async def post_task(
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.post(db, user, payload)


@router.patch("/{id}/", response_model=TaskCreateDB)
async def patch_task(
    id: int,
    payload: TaskPut,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.patch(db, user, payload, id)


@router.delete("/{id}/")
async def delete_task(
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.delete(db, user, id)
