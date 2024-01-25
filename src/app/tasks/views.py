from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.idps import crud
from app.idps.schemas import IdpDB

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[IdpDB])
async def get_all_tasks(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)


@router.get("/{id}/", response_model=IdpDB)
async def get_task(id: int, db: AsyncSession = Depends(get_db)):
    idp = await crud.get_by_id(db, id)
    if not idp:
        raise HTTPException(status_code=404, detail="Idp not found")
    return idp
