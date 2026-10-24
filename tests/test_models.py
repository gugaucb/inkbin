from datetime import UTC, datetime

import pytest
from sqlalchemy import select

from inkbin.db import get_engine, get_session_maker, init_db
from inkbin.models import Paste


@pytest.mark.asyncio
async def test_paste_model_persistence():
    engine = get_engine("sqlite+aiosqlite:///:memory:")
    await init_db(engine)
    session_factory = get_session_maker(engine)

    async with session_factory() as session:
        paste = Paste(
            slug="AbC123x",
            title="Meu Script Python",
            content="print('Hello Inkbin')",
            language="python",
            admin_delete_hash="dummyhash123",
            views_count=0,
            expires_at=None,
            created_at=datetime.now(UTC),
        )
        session.add(paste)
        await session.commit()

        # Query back
        stmt = select(Paste).where(Paste.slug == "AbC123x")
        result = await session.execute(stmt)
        saved = result.scalar_one_or_none()

        assert saved is not None
        assert saved.slug == "AbC123x"
        assert saved.title == "Meu Script Python"
        assert saved.content == "print('Hello Inkbin')"
        assert saved.language == "python"
        assert saved.views_count == 0
        assert saved.expires_at is None
        assert saved.id is not None
        assert saved.content_format == "plaintext"
        assert saved.burn_after_read is False

    await engine.dispose()


@pytest.mark.asyncio
async def test_paste_model_custom_format_and_burn():
    engine = get_engine("sqlite+aiosqlite:///:memory:")
    await init_db(engine)
    session_factory = get_session_maker(engine)

    async with session_factory() as session:
        paste = Paste(
            slug="Sec1234",
            title="Encrypted Secret",
            content="ciphertext_payload_base64",
            language="python",
            content_format="aes-256-gcm",
            burn_after_read=True,
            admin_delete_hash="dummyhash123",
            views_count=0,
            expires_at=None,
            created_at=datetime.now(UTC),
        )
        session.add(paste)
        await session.commit()

        stmt = select(Paste).where(Paste.slug == "Sec1234")
        result = await session.execute(stmt)
        saved = result.scalar_one_or_none()

        assert saved is not None
        assert saved.content_format == "aes-256-gcm"
        assert saved.burn_after_read is True

    await engine.dispose()
