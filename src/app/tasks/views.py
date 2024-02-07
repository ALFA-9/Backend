from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Employee
from app.database.session import get_db
from app.employees.views import get_current_auth_user
from app.tasks import crud
from app.tasks.schemas import (CommentCreate, CommentCreateDB, TaskCreate,
                               TaskCreateDB, TaskPut)

router = APIRouter(prefix="/tasks", tags=["tasks"])


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


@router.post("/{id}/comments/", response_model=CommentCreateDB)
async def post_comment(
    id: int,
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.post_comment(db, user, id, payload)
