import hashlib

import pytest
from sqlalchemy import select

from inkbin.cache import get_cache_service
from inkbin.models import Paste


def test_sha256_content_hash_formula():
    text = "Hello, Inkbin World!"
    expected_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert len(expected_hash) == 64
    assert expected_hash == "b53fdcac42fe9e105429af9961e4351a8d1d82e675b82dea29a3957c5edf9429"


@pytest.mark.asyncio
async def test_duplicate_submission_within_60s_triggers_429(client, test_session_factory):
    cache = get_cache_service()
    await cache.clear()

    payload = {
        "title": "Spam Test",
        "content": "REPEAT REPEAT REPEAT CONTENT",
        "language": "plaintext",
    }

    # 1. First submission succeeds
    res1 = await client.post(
        "/api/pastes", json=payload, headers={"X-Forwarded-For": "203.0.113.10"}
    )
    assert res1.status_code == 201
    slug1 = res1.json()["slug"]

    # Check content_hash in database
    async with test_session_factory() as session:
        stmt = select(Paste).where(Paste.slug == slug1)
        res = await session.execute(stmt)
        paste = res.scalar_one()
        assert paste.content_hash == hashlib.sha256(payload["content"].encode("utf-8")).hexdigest()

    # 2. Second identical submission within 60s from same IP is rejected with 429
    res2 = await client.post(
        "/api/pastes", json=payload, headers={"X-Forwarded-For": "203.0.113.10"}
    )
    assert res2.status_code == 429
    assert "Retry-After" in res2.headers
    assert int(res2.headers["Retry-After"]) > 0
    assert "duplicado" in res2.json()["detail"].lower() or slug1 in res2.json()["detail"]


@pytest.mark.asyncio
async def test_different_content_from_same_ip_allowed(client):
    cache = get_cache_service()
    await cache.clear()

    res1 = await client.post(
        "/api/pastes",
        json={"content": "Content Alpha"},
        headers={"X-Forwarded-For": "203.0.113.20"},
    )
    assert res1.status_code == 201

    res2 = await client.post(
        "/api/pastes",
        json={"content": "Content Beta"},
        headers={"X-Forwarded-For": "203.0.113.20"},
    )
    assert res2.status_code == 201
    assert res1.json()["slug"] != res2.json()["slug"]


@pytest.mark.asyncio
async def test_identical_content_from_different_ips_allowed(client):
    cache = get_cache_service()
    await cache.clear()

    same_content = "Shared boiler plate code snippet"

    res1 = await client.post(
        "/api/pastes",
        json={"content": same_content},
        headers={"X-Forwarded-For": "203.0.113.31"},
    )
    assert res1.status_code == 201

    res2 = await client.post(
        "/api/pastes",
        json={"content": same_content},
        headers={"X-Forwarded-For": "203.0.113.32"},
    )
    assert res2.status_code == 201


@pytest.mark.asyncio
async def test_submission_after_window_expires_allowed(client):
    cache = get_cache_service()
    await cache.clear()

    content = "Single submission to expire"
    headers = {"X-Forwarded-For": "203.0.113.40"}

    res1 = await client.post("/api/pastes", json={"content": content}, headers=headers)
    assert res1.status_code == 201

    # Simulate expiration by clearing cache
    await cache.clear()

    # Submission now allowed again
    res2 = await client.post("/api/pastes", json={"content": content}, headers=headers)
    assert res2.status_code == 201
