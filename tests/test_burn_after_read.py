import pytest
from httpx import AsyncClient
from sqlalchemy import select

from inkbin.models import Paste


@pytest.mark.asyncio
async def test_burn_after_read_lifecycle(client: AsyncClient, test_session_factory):
    # 1. Create a paste with burn_after_read=True via API
    create_payload = {
        "title": "Secret Doc",
        "content": "Confidential payload content",
        "language": "python",
        "expiration": "never",
        "burn_after_read": True,
    }
    res_create = await client.post("/api/pastes", json=create_payload)
    assert res_create.status_code == 201
    created_data = res_create.json()
    slug = created_data["slug"]
    assert created_data["burn_after_read"] is True

    # 2. GET /p/{slug} should render the interstitial confirmation screen without deleting
    res_get = await client.get(f"/p/{slug}")
    assert res_get.status_code == 200
    html_get = res_get.text
    assert (
        "burn-reveal-form" in html_get
        or "burn_confirmation" in html_get
        or "Reveal and Destroy" in html_get
        or "Revelar e Destruir" in html_get
    )
    assert "Confidential payload content" not in html_get

    # Verify paste is still present in database
    async with test_session_factory() as session:
        res_db = await session.execute(select(Paste).where(Paste.slug == slug))
        assert res_db.scalar_one_or_none() is not None

    # 3. POST /p/{slug}/reveal should reveal the content and purge the record
    res_reveal = await client.post(f"/p/{slug}/reveal")
    assert res_reveal.status_code == 200
    html_reveal = res_reveal.text
    assert "Confidential payload content" in html_reveal
    assert (
        "permanently purged" in html_reveal
        or "destruído permanentemente" in html_reveal
        or "永久清除" in html_reveal
    )

    # Verify paste is permanently purged from database
    async with test_session_factory() as session:
        res_db_after = await session.execute(select(Paste).where(Paste.slug == slug))
        assert res_db_after.scalar_one_or_none() is None

    # 4. Subsequent access must return 404 Not Found immediately
    res_subsequent = await client.get(f"/p/{slug}")
    assert res_subsequent.status_code == 404


@pytest.mark.asyncio
async def test_burn_after_read_api_confirmation(client: AsyncClient):
    # Create paste with burn_after_read=True
    create_payload = {
        "title": "API Secret",
        "content": "API payload secret",
        "language": "plaintext",
        "expiration": "1d",
        "burn_after_read": True,
    }
    res_create = await client.post("/api/pastes", json=create_payload)
    assert res_create.status_code == 201
    slug = res_create.json()["slug"]

    # Access without confirm_burn should be blocked (HTTP 400 or interstitial notice)
    res_api_blocked = await client.get(f"/api/pastes/{slug}")
    assert res_api_blocked.status_code == 400
    assert "confirm_burn" in res_api_blocked.json()["detail"]

    # Access with confirm_burn=true reveals and deletes
    res_api_reveal = await client.get(f"/api/pastes/{slug}?confirm_burn=true")
    assert res_api_reveal.status_code == 200
    assert res_api_reveal.json()["content"] == "API payload secret"

    # Subsequent access is 404
    res_api_404 = await client.get(f"/api/pastes/{slug}?confirm_burn=true")
    assert res_api_404.status_code == 404


@pytest.mark.asyncio
async def test_burn_after_read_time_expiration(client: AsyncClient, test_session_factory):
    from datetime import UTC, datetime, timedelta

    from sqlalchemy import update

    # 1. Create a paste with burn_after_read=True
    create_payload = {
        "title": "Expiring Secret",
        "content": "Secret will expire before read",
        "language": "python",
        "expiration": "1h",
        "burn_after_read": True,
    }
    res_create = await client.post("/api/pastes", json=create_payload)
    assert res_create.status_code == 201
    slug = res_create.json()["slug"]

    # 2. Simulate expiration in the past
    past_time = datetime.now(UTC) - timedelta(hours=2)
    async with test_session_factory() as session:
        await session.execute(update(Paste).where(Paste.slug == slug).values(expires_at=past_time))
        await session.commit()

    # 3. GET /p/{slug} should return 404 (expired) without showing confirmation
    res_get = await client.get(f"/p/{slug}")
    assert res_get.status_code == 404

    # 4. POST /p/{slug}/reveal should also return 404
    res_reveal = await client.post(f"/p/{slug}/reveal")
    assert res_reveal.status_code == 404
