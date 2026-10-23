from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy import inspect, text
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


def _sync_migrate_schema(connection) -> None:
    """Aplica migrações incrementais para garantir paridade de esquema com os modelos."""
    inspector = inspect(connection)
    table_names = inspector.get_table_names()
    if "pastes" in table_names:
        existing_cols = {col["name"] for col in inspector.get_columns("pastes")}
        is_postgres = connection.dialect.name == "postgresql"
        bool_false = "FALSE" if is_postgres else "0"
        bool_true = "TRUE" if is_postgres else "1"

        if "is_protected" not in existing_cols:
            connection.execute(
                text(
                    f"ALTER TABLE pastes ADD COLUMN is_protected BOOLEAN DEFAULT {bool_false} NOT NULL"
                )
            )
        if "password_hash" not in existing_cols:
            connection.execute(text("ALTER TABLE pastes ADD COLUMN password_hash VARCHAR(255)"))
        if "content_hash" not in existing_cols:
            connection.execute(text("ALTER TABLE pastes ADD COLUMN content_hash VARCHAR(64)"))
            connection.execute(
                text("CREATE INDEX IF NOT EXISTS ix_pastes_content_hash ON pastes (content_hash)")
            )
        if "report_count" not in existing_cols:
            connection.execute(
                text("ALTER TABLE pastes ADD COLUMN report_count INTEGER DEFAULT 0 NOT NULL")
            )
        if "is_active" not in existing_cols:
            connection.execute(
                text(
                    f"ALTER TABLE pastes ADD COLUMN is_active BOOLEAN DEFAULT {bool_true} NOT NULL"
                )
            )


async def init_db(engine: AsyncEngine | None = None) -> None:
    """Cria todas as tabelas registradas no metadata e aplica migrações incrementais."""
    if engine is None:
        engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_sync_migrate_schema)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency do FastAPI para injeção de sessão assíncrona."""
    session_factory = get_session_maker()
    async with session_factory() as session:
        yield session
