from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import utils as auth_utils
from app.database.session import get_db
from app.employees import crud
from app.employees.schemas import EmployeeDB

http_bearer = HTTPBearer()


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/auth", tags=["Auth"])


async def validate_auth_user(
    user_email: str = Form(),
    db: AsyncSession = Depends(get_db),
) -> EmployeeDB:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email",
    )
    if not (user := await crud.get_by_email(db, user_email)):
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


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    db: AsyncSession = Depends(get_db),
) -> EmployeeDB:
    user_email: str | None = payload.get("sub")
    if user := await crud.get_by_email(db, user_email):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: EmployeeDB = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
