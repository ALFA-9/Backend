from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.tasks import crud
from app.tasks.schemas import TaskCreate, TaskCreateDB, TaskDB

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskDB])
async def get_all_tasks(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)


@router.get("/{id}/", response_model=TaskDB)
async def get_task(id: int, db: AsyncSession = Depends(get_db)):
    idp = await crud.get_by_id(db, id)
    if not idp:
        raise HTTPException(status_code=404, detail="Idp not found")
    return idp


@router.post("/", response_model=TaskCreateDB)
async def post_idp(payload: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.post(db, payload)
