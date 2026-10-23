import pytest

from inkbin.db import get_engine, get_session_maker, init_db
from inkbin.services import SlugCollisionError, create_paste_record


@pytest.mark.asyncio
async def test_slug_collision_retry_success():
    engine = get_engine("sqlite+aiosqlite:///:memory:")
    await init_db(engine)
    session_factory = get_session_maker(engine)

    # First create a paste with slug "collision"
    async with session_factory() as session:
        await create_paste_record(
            session=session,
            title="First",
            content="content1",
            language="plaintext",
            slug_generator=lambda: "collision",
        )

    # Now attempt creating a second paste where first try returns "collision", second returns "unique"
    slug_sequence = ["collision", "unique12"]

    def mock_generator():
        return slug_sequence.pop(0)

    async with session_factory() as session:
        paste, token = await create_paste_record(
            session=session,
            title="Second",
            content="content2",
            language="plaintext",
            slug_generator=mock_generator,
        )
        assert paste.slug == "unique12"
        assert token is not None

    await engine.dispose()


@pytest.mark.asyncio
async def test_slug_collision_max_retries_exceeded():
    engine = get_engine("sqlite+aiosqlite:///:memory:")
    await init_db(engine)
    session_factory = get_session_maker(engine)

    # Pre-create "collide"
    async with session_factory() as session:
        await create_paste_record(
            session=session,
            title="Original",
            content="content",
            language="plaintext",
            slug_generator=lambda: "collide",
        )

    # Attempt with generator that always returns "collide"
    async with session_factory() as session:
        with pytest.raises(SlugCollisionError):
            await create_paste_record(
                session=session,
                title="Fail",
                content="content",
                language="plaintext",
                slug_generator=lambda: "collide",
                max_retries=3,
            )

    await engine.dispose()
