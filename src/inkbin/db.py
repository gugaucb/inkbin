from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from inkbin.config import get_settings


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine(database_url: str | None = None) -> AsyncEngine:
    if database_url is None:
        database_url = get_settings().DATABASE_URL
    return create_async_engine(
        database_url,
        echo=False,
        future=True,
    )


def get_session_maker(engine: AsyncEngine | None = None) -> async_sessionmaker[AsyncSession]:
    if engine is None:
        engine = get_engine()
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


async def init_db(engine: AsyncEngine | None = None) -> None:
    """Cria todas as tabelas registradas no metadata."""
    if engine is None:
        engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency do FastAPI para injeção de sessão assíncrona."""
    session_factory = get_session_maker()
    async with session_factory() as session:
        yield session
