from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select

from inkbin.cache import get_cache_service
from inkbin.lifecycle import purge_expired_pastes
from inkbin.models import Paste
from inkbin.schemas import ExpirationEnum
from inkbin.services import create_paste_record


def test_expiration_enum_calculations():
    now = datetime.now(UTC)
    assert ExpirationEnum.never.to_datetime() is None

    exp_1h = ExpirationEnum.one_hour.to_datetime()
    assert exp_1h is not None
    assert 3500 < (exp_1h - now).total_seconds() < 3700

    exp_1d = ExpirationEnum.one_day.to_datetime()
    assert exp_1d is not None
    assert 86300 < (exp_1d - now).total_seconds() < 86500

    exp_1w = ExpirationEnum.one_week.to_datetime()
    assert exp_1w is not None
    assert 604700 < (exp_1w - now).total_seconds() < 604900

    exp_1m = ExpirationEnum.one_month.to_datetime()
    assert exp_1m is not None
    assert 2591900 < (exp_1m - now).total_seconds() < 2592100


@pytest.mark.asyncio
async def test_on_demand_expiration_returns_404_and_purges(client, test_session_factory):
    # Create paste with expiration in the past
    now = datetime.now(UTC)
    past = now - timedelta(hours=2)

    async with test_session_factory() as session:
        paste, _ = await create_paste_record(
            session=session,
            title="Expired Paste",
            content="This should not be readable",
            expires_at=past,
        )
        slug = paste.slug

    # 1. API GET must return 404
    api_res = await client.get(f"/api/pastes/{slug}")
    assert api_res.status_code == 404

    # 2. Raw GET must return 404
    raw_res = await client.get(f"/raw/{slug}")
    assert raw_res.status_code == 404

    # 3. Web GET must return 404
    web_res = await client.get(f"/p/{slug}")
    assert web_res.status_code == 404

    # 4. Check DB: on-demand must have purged the record
    async with test_session_factory() as session:
        stmt = select(Paste).where(Paste.slug == slug)
        res = await session.execute(stmt)
        assert res.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_sweep_runner_purges_expired_and_preserves_valid(test_session_factory):
    cache = get_cache_service()
    await cache.clear()

    now = datetime.now(UTC)
    past_time = now - timedelta(hours=3)
    future_time = now + timedelta(hours=3)

    async with test_session_factory() as session:
        # Expired pastes
        p1, _ = await create_paste_record(
            session, title="Expired 1", content="c1", expires_at=past_time
        )
        p2, _ = await create_paste_record(
            session, title="Expired 2", content="c2", expires_at=past_time
        )
        # Active pastes
        p3, _ = await create_paste_record(
            session, title="Active Future", content="c3", expires_at=future_time
        )
        p4, _ = await create_paste_record(
            session, title="Active Never", content="c4", expires_at=None
        )

        slug1, slug2, slug3, slug4 = p1.slug, p2.slug, p3.slug, p4.slug

    # Set cache entries for all
    await cache.set(f"paste:{slug1}", "cached_1")
    await cache.set(f"paste:{slug2}", "cached_2")
    await cache.set(f"paste:{slug3}", "cached_3")
    await cache.set(f"paste:{slug4}", "cached_4")

    # Run sweep runner
    async with test_session_factory() as session:
        purged = await purge_expired_pastes(session, cache)
        assert purged == 2

    # Verify database state
    async with test_session_factory() as session:
        stmt = select(Paste.slug)
        res = await session.execute(stmt)
        remaining_slugs = set(res.scalars().all())
        assert slug1 not in remaining_slugs
        assert slug2 not in remaining_slugs
        assert slug3 in remaining_slugs
        assert slug4 in remaining_slugs

    # Verify cache eviction
    assert await cache.get(f"paste:{slug1}") is None
    assert await cache.get(f"paste:{slug2}") is None
    assert await cache.get(f"paste:{slug3}") == "cached_3"
    assert await cache.get(f"paste:{slug4}") == "cached_4"


@pytest.mark.asyncio
async def test_sweep_runner_empty(test_session_factory):
    async with test_session_factory() as session:
        purged = await purge_expired_pastes(session)
        assert purged == 0
