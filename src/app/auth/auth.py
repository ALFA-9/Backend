from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import utils as auth_utils
from app.database.models import Employee
from app.database.session import get_db
from app.employees import crud

http_bearer = HTTPBearer()


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class EmailData(BaseModel):
    email: str


router = APIRouter(prefix="/auth", tags=["Auth"])


async def validate_auth_user(
    payload: EmailData = Body(),
    db: AsyncSession = Depends(get_db),
) -> Employee:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email",
    )
    if not (user := await crud.get_by_email(db, payload.email)):
        raise unauthed_exc
    return user


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> dict:
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error",
        )
    return payload


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: Employee = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
