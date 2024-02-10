import datetime as dt

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.idps import crud
from app.api_v1.idps.schemas import (IdpCreate, IdpCreateDB, IdpList, IdpPatch,
                                     IdpRetrieve, RequestSchema)
from app.auth.auth import get_current_auth_user
from app.constants import (EXAMPLE_403, EXAMPLE_429, EXAMPLE_ACTIVE_IDP_400,
                           EXAMPLE_ERROR_SENDING_400, EXAMPLE_IDP_404,
                           EXAMPLE_SUCCESS_SENDING_200,
                           SEC_BEFORE_NEXT_REQUEST, SUBJECT)
from app.database.models import Employee
from app.database.session import get_db
from app.utils import get_all_parents_id, send_email

router = APIRouter(prefix="/idps", tags=["idps"])


@router.get("/", response_model=list[IdpList])
async def get_all_idps(
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    return await crud.get_all(db, user)


@router.get(
    "/{id}/",
    response_model=IdpRetrieve,
    responses={
        404: EXAMPLE_IDP_404,
    },
)
async def get_idp(
    id: int,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    idp = await crud.get_by_id(db, user, id)
    if not idp:
        raise HTTPException(status_code=404, detail="IDP not found")
    return idp


@router.post(
    "/",
    response_model=IdpCreateDB,
    responses={
        403: EXAMPLE_403,
        400: EXAMPLE_ACTIVE_IDP_400,
    },
)
async def post_idp(
    payload: IdpCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    result = await crud.post(db, user, payload)
    background_tasks.add_task(
        send_email,
        SUBJECT,
        "У вас новый ИПР.",
        result.employee.email,
    )
    return result


@router.patch(
    "/{id}/",
    response_model=IdpCreateDB,
    responses={
        403: EXAMPLE_403,
        404: EXAMPLE_IDP_404,
    },
)
async def patch_idp(
    id: int,
    payload: IdpPatch,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    result = await crud.patch(db, user, payload, id)
    background_tasks.add_task(
        send_email,
        SUBJECT,
        "Статус вашего ИПР изменен.",
        result.employee.email,
    )
    return result


@router.post(
    "/request/",
    responses={
        200: EXAMPLE_SUCCESS_SENDING_200,
        403: EXAMPLE_403,
        400: EXAMPLE_ERROR_SENDING_400,
        429: EXAMPLE_429,
    },
)
async def post_request(
    payload: RequestSchema = Depends(),
    db: AsyncSession = Depends(get_db),
    user: Employee = Depends(get_current_auth_user),
):
    if user.last_request:
        diff = dt.datetime.now() - user.last_request
        if diff.total_seconds() < SEC_BEFORE_NEXT_REQUEST:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="You cant send more than 1 request per day",
            )
    if "in_work" in [idp.status_idp.value for idp in user.idp_emp]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee already has active IDP",
        )
    directors_id = get_all_parents_id(user.id)
    statement = (
        select(Employee)
        .filter(Employee.id.in_(select(directors_id)))
        .where(Employee.id == payload.director_id)
    )
    result = await db.execute(statement)
    if (director := result.scalar()) is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )
    try:
        await send_email(
            payload.title,
            payload.letter,
            payload.files,
            director.email,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mail didnt sent",
        )
    result = jsonable_encoder(payload)
    if result["files"]:
        result["files"] = [x["filename"] for x in result["files"]]
    return JSONResponse(content=result)
