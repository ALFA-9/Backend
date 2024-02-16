from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import settings

# SQLAlchemy
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Для импорта данных
sync_engine = create_engine(
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}"
)

SessionLocal = sessionmaker(
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)


async def get_db():
    async with SessionLocal() as session:
        yield session
        await session.close()
