import asyncio

import pytest
from httpx import AsyncClient

from inkbin.cache import InMemoryCache, get_cache_service
from inkbin.rate_limit import InMemoryRateLimiter, get_rate_limiter


@pytest.mark.asyncio
async def test_in_memory_cache_get_set_ttl():
    cache = InMemoryCache()
    await cache.set("test_key", "hello", ttl_seconds=1)
    val = await cache.get("test_key")
    assert val == "hello"

    # Test expiration
    await asyncio.sleep(1.05)
    expired_val = await cache.get("test_key")
    assert expired_val is None


@pytest.mark.asyncio
async def test_in_memory_cache_delete():
    cache = InMemoryCache()
    await cache.set("k1", "v1")
    await cache.delete("k1")
    assert await cache.get("k1") is None


@pytest.mark.asyncio
async def test_in_memory_rate_limiter_allows_and_blocks():
    limiter = InMemoryRateLimiter()
    ip = "192.168.1.100"

    # Allow up to 3 requests
    for _ in range(3):
        allowed, retry_after = await limiter.is_allowed(ip, limit=3, window_seconds=10)
        assert allowed is True
        assert retry_after == 0

    # 4th request should be blocked
    allowed, retry_after = await limiter.is_allowed(ip, limit=3, window_seconds=10)
    assert allowed is False
    assert retry_after > 0


@pytest.mark.asyncio
async def test_cache_service_hit_in_api(client: AsyncClient):
    create_res = await client.post(
        "/api/pastes",
        json={"title": "Cached Paste", "content": "print('cached')", "language": "python"},
    )
    assert create_res.status_code == 201
    slug = create_res.json()["slug"]

    # Initial get (caches)
    get1 = await client.get(f"/api/pastes/{slug}")
    assert get1.status_code == 200

    # Verify cached entry exists
    cache = get_cache_service()
    cached_val = await cache.get(f"paste:{slug}")
    assert cached_val is not None
    assert "Cached Paste" in cached_val

    # Second get should retrieve with incremented view count
    get2 = await client.get(f"/api/pastes/{slug}")
    assert get2.status_code == 200
    assert get2.json()["views_count"] == 2


@pytest.mark.asyncio
async def test_rate_limit_middleware_429(client: AsyncClient):
    limiter = get_rate_limiter()
    ip = "198.51.100.42"
    headers = {"X-Forwarded-For": ip}

    # Simulate exhausting the limit
    for _ in range(100):
        await limiter.is_allowed(key=ip, limit=100, window_seconds=60)

    # Next request to an API endpoint with that IP should receive 429
    res = await client.post(
        "/api/pastes",
        json={"content": "test rate limit"},
        headers=headers,
    )
    assert res.status_code == 429
    assert "Retry-After" in res.headers
    assert res.json()["detail"] == "Too Many Requests. Limite de requisições excedido."
