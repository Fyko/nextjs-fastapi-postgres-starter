import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARN)

_main_uri = "postgres:postgres@localhost:5432/postgres"
_sync_uri = f"postgresql://{_main_uri}"
_async_uri = f"postgresql+asyncpg://{_main_uri}"

sync_engine = create_engine(_sync_uri)
engine = create_async_engine(_async_uri)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def migrate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        yield session
