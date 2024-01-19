from app.database.db import get_db
from app.api.idps import crud
from app.api.idps.models import IdpDB
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get('/', response_model=list[IdpDB])
async def get_all_idps(db: AsyncSession = Depends(get_db)):
    return await crud.get_all(db)


@router.get("/{id}/", response_model=IdpDB)
async def get_idp(id: int, db: AsyncSession = Depends(get_db)):
    employee = await crud.get_by_id(db, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Idp not found")
    return employee
