from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Employee
from app.database.session import get_db
from app.employees.views import get_current_auth_user
from app.idps import crud
from app.idps.schemas import (IdpCreate, IdpCreateDB, IdpList, IdpPut,
                              IdpRetrieve, RequestSchema)

router = APIRouter(prefix="/idps", tags=["idps"])


@router.get("/", response_model=list[IdpList])
async def get_all_idps(
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.get_all(db, user)


@router.get("/{id}/", response_model=IdpRetrieve)
async def get_idp(
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    idp = await crud.get_by_id(db, user, id)
    if not idp:
        raise HTTPException(status_code=404, detail="Idp not found")
    return idp


@router.post("/", response_model=IdpCreateDB)
async def post_idp(
    payload: IdpCreate,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.post(db, user, payload)


@router.patch("/{id}/", response_model=IdpCreateDB)
async def patch_idp(
    id: int,
    payload: IdpPut,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.patch(db, user, payload, id)


@router.post("/request/")
async def post_request(
    payload: RequestSchema = Depends(),
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    result = await crud.post_request(db, user, payload)
    result = jsonable_encoder(result)
    if result["files"]:
        result["files"] = [x["filename"] for x in result["files"]]
    return JSONResponse(content=result)
