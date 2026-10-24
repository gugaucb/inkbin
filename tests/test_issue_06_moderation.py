import pytest
from sqlalchemy import select

from inkbin.cache import get_cache_service
from inkbin.config import get_settings
from inkbin.models import Paste


@pytest.mark.asyncio
async def test_report_paste_success(client, test_session_factory):
    cache = get_cache_service()
    await cache.clear()

    # 1. Create a paste
    create_res = await client.post(
        "/api/pastes",
        json={"title": "Abusive Paste", "content": "Bad malicious payload"},
    )
    assert create_res.status_code == 201
    slug = create_res.json()["slug"]

    # 2. Report the paste
    report_res = await client.post(
        f"/api/pastes/{slug}/report",
        json={"reason": "malware", "details": "Suspicious backdoor code detected"},
        headers={"X-Forwarded-For": "203.0.113.100"},
    )
    assert report_res.status_code == 200
    assert report_res.json()["report_count"] == 1

    # 3. Verify in DB
    async with test_session_factory() as session:
        stmt = select(Paste).where(Paste.slug == slug)
        res = await session.execute(stmt)
        paste = res.scalar_one()
        assert paste.report_count == 1
        assert paste.is_active is True


@pytest.mark.asyncio
async def test_report_rate_limit(client):
    cache = get_cache_service()
    await cache.clear()

    create_res = await client.post(
        "/api/pastes",
        json={"content": "Content to report multiple times"},
    )
    slug = create_res.json()["slug"]
    headers = {"X-Forwarded-For": "203.0.113.101"}

    # First 5 reports succeed
    for i in range(5):
        res = await client.post(
            f"/api/pastes/{slug}/report",
            json={"reason": "spam"},
            headers=headers,
        )
        assert res.status_code == 200

    # 6th report is rate limited
    res6 = await client.post(
        f"/api/pastes/{slug}/report",
        json={"reason": "spam"},
        headers=headers,
    )
    assert res6.status_code == 429
    assert "Retry-After" in res6.headers


@pytest.mark.asyncio
async def test_admin_deactivation_flow(client):
    settings = get_settings()
    master_token = settings.SECRET_KEY

    # 1. Create paste and cache it
    create_res = await client.post(
        "/api/pastes",
        json={"title": "Notice of Removal", "content": "Infringing material"},
    )
    slug = create_res.json()["slug"]

    # Populate cache
    assert (await client.get(f"/api/pastes/{slug}")).status_code == 200

    # 2. Attempt deactivation with invalid operator token
    invalid_res = await client.patch(
        f"/api/pastes/{slug}/deactivate",
        headers={"X-Operator-Token": "bad-operator-token"},
    )
    assert invalid_res.status_code == 403

    # 3. Deactivate with valid operator token
    deact_res = await client.patch(
        f"/api/pastes/{slug}/deactivate",
        headers={"X-Operator-Token": master_token},
    )
    assert deact_res.status_code == 200
    assert deact_res.json()["is_active"] is False

    # 4. Now reading returns HTTP 451
    api_res = await client.get(f"/api/pastes/{slug}")
    assert api_res.status_code == 451

    raw_res = await client.get(f"/raw/{slug}")
    assert raw_res.status_code == 451

    web_res = await client.get(f"/p/{slug}")
    assert web_res.status_code == 451
    assert (
        "deactivated" in web_res.text.lower()
        or "desativado" in web_res.text.lower()
        or "violation" in web_res.text.lower()
        or "violação" in web_res.text.lower()
    )
