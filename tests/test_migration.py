from datetime import UTC, datetime

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from inkbin.db import init_db
from inkbin.models import Paste


@pytest.mark.asyncio
async def test_init_db_migrates_legacy_pastes_table():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    # 1. Simulate legacy database schema without security/moderation columns
    async with engine.begin() as conn:
        await conn.execute(
            text(
                """
                CREATE TABLE pastes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug VARCHAR(8) UNIQUE NOT NULL,
                    title VARCHAR(200),
                    content TEXT NOT NULL,
                    language VARCHAR(50) NOT NULL,
                    admin_delete_hash VARCHAR(128) NOT NULL,
                    views_count INTEGER NOT NULL,
                    expires_at TIMESTAMP,
                    created_at TIMESTAMP NOT NULL
                )
                """
            )
        )
        await conn.execute(
            text(
                """
                INSERT INTO pastes (slug, title, content, language, admin_delete_hash, views_count, created_at)
                VALUES ('legacy1', 'Old Title', 'Old Content', 'plaintext', 'hash123', 0, '2026-10-23 12:00:00')
                """
            )
        )

    # 2. Run init_db which should migrate the existing legacy table
    await init_db(engine)

    session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        # Existing record should be readable with default values for new columns
        res = await session.execute(select(Paste).where(Paste.slug == "legacy1"))
        legacy_paste = res.scalar_one_or_none()
        assert legacy_paste is not None
        assert legacy_paste.is_protected is False
        assert legacy_paste.is_active is True
        assert legacy_paste.report_count == 0

        # New records with new columns can be inserted without UndefinedColumn / OperationalError
        new_paste = Paste(
            slug="new1234",
            title="New Protected Paste",
            content="Sensitive data",
            language="python",
            admin_delete_hash="delhash",
            views_count=0,
            expires_at=None,
            created_at=datetime.now(UTC),
            is_protected=True,
            password_hash="argon2id$mockhash",
            content_hash="sha256hash",
            report_count=0,
            is_active=True,
        )
        session.add(new_paste)
        await session.commit()

        # Query back new paste
        res_new = await session.execute(select(Paste).where(Paste.slug == "new1234"))
        saved_new = res_new.scalar_one_or_none()
        assert saved_new is not None
        assert saved_new.is_protected is True
        assert saved_new.password_hash == "argon2id$mockhash"
        assert saved_new.content_hash == "sha256hash"

    await engine.dispose()
