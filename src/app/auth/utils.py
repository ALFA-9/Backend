from datetime import datetime, timedelta

import jwt

from config import auth


def encode_jwt(
    payload: dict,
    private_key: str = auth.private_key_path.read_text(),
    algorithm: str = auth.algorithm,
    expire_minutes: int = auth.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = auth.public_key_path.read_text(),
    algorithm: str = auth.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded
