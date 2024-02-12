import os
from pathlib import Path

from pydantic import BaseModel

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseModel):
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    SMTP_HOST: str | None = os.getenv("SMTP_HOST", None)
    SMTP_PORT: int | None = os.getenv("SMTP_PORT", None)
    SMTP_USER: str | None = os.getenv("SMTP_USER", None)
    SMTP_PASSWORD: str | None = os.getenv("SMTP_PASSWORD", None)
    EMAILS_FROM_EMAIL: str | None = os.getenv("EMAILS_FROM_EMAIL", None)
    EMAILS_ENABLED: bool = False

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", 5432)
    DATABASE_URL: str = os.getenv("DATABASE_URL")


auth = AuthJWT()
settings = Settings()
