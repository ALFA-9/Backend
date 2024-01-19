import os

from databases import Database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_async_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine,
)


async def get_db():
    async with SessionLocal() as session:
        yield session

# databases query builder
database = Database(DATABASE_URL)
