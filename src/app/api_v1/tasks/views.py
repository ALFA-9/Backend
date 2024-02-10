from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.tasks import crud
from app.api_v1.tasks.schemas import (CommentCreate, CommentCreateDB,
                                      TaskCreate, TaskCreateDB, TaskPatch)
from app.auth.auth import get_current_auth_user
from app.constants import EXAMPLE_403, EXAMPLE_IDP_404, EXAMPLE_TASK_404
from app.database.models import Employee
from app.database.session import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=TaskCreateDB,
    responses={
        403: EXAMPLE_403,
        404: EXAMPLE_IDP_404,
    },
)
async def post_task(
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.post(db, user, payload)


@router.patch(
    "/{id}/",
    response_model=TaskCreateDB,
    responses={
        403: EXAMPLE_403,
        404: EXAMPLE_TASK_404,
    },
)
async def patch_task(
    id: int,
    payload: TaskPatch,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.patch(db, user, payload, id, background_tasks)


@router.delete(
    "/{id}/",
    responses={
        403: EXAMPLE_403,
        404: EXAMPLE_TASK_404,
    },
)
async def delete_task(
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.delete(db, user, id)


@router.post(
    "/{id}/comments/",
    response_model=CommentCreateDB,
    responses={
        403: EXAMPLE_403,
        404: EXAMPLE_TASK_404,
    },
)
async def post_comment(
    id: int,
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.post_comment(db, user, id, payload)
