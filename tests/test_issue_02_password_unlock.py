import pytest

from inkbin.cache import get_cache_service


@pytest.mark.asyncio
async def test_unlock_success_sets_cookie_and_grants_access(client):
    # 1. Create protected paste
    create_res = await client.post(
        "/api/pastes",
        json={
            "title": "Secret Doc",
            "content": "TOP SECRET CODE 007",
            "language": "python",
            "password": "CorrectPassword123",
        },
    )
    assert create_res.status_code == 201
    slug = create_res.json()["slug"]

    # 2. Before unlock, raw and api return 401
    assert (await client.get(f"/raw/{slug}")).status_code == 401
    assert (await client.get(f"/api/pastes/{slug}")).status_code == 401

    # 3. Post correct password to unlock endpoint
    unlock_res = await client.post(
        f"/api/pastes/{slug}/unlock",
        json={"password": "CorrectPassword123"},
    )
    assert unlock_res.status_code == 200
    assert unlock_res.json()["unlocked"] is True
    cookie_name = f"inkbin_unlocked_{slug}"
    assert cookie_name in unlock_res.cookies

    # 4. Use client with cookie
    client.cookies.set(cookie_name, unlock_res.cookies[cookie_name])

    # 5. Now raw returns 200 and content
    raw_res = await client.get(f"/raw/{slug}")
    assert raw_res.status_code == 200
    assert raw_res.text == "TOP SECRET CODE 007"

    # 6. Now api returns 200 and content
    api_res = await client.get(f"/api/pastes/{slug}")
    assert api_res.status_code == 200
    assert api_res.json()["content"] == "TOP SECRET CODE 007"

    # 7. Web viewer returns 200 with code
    web_res = await client.get(f"/p/{slug}")
    assert web_res.status_code == 200
    assert "TOP SECRET CODE 007" in web_res.text


@pytest.mark.asyncio
async def test_unlock_invalid_password_decrements_attempts_and_locks_out(client):
    cache = get_cache_service()
    await cache.clear()

    create_res = await client.post(
        "/api/pastes",
        json={
            "content": "Classified Information",
            "password": "MySecretVault99",
        },
    )
    slug = create_res.json()["slug"]

    # Attempts 1 to 4 should return 401 with decreasing remaining attempts
    for attempt in range(1, 5):
        res = await client.post(
            f"/api/pastes/{slug}/unlock",
            json={"password": "WrongPassword!"},
        )
        assert res.status_code == 401
        expected_remaining = 5 - attempt
        assert str(expected_remaining) in res.json()["detail"]

    # Attempt 5 should return 429 (lockout triggered)
    res5 = await client.post(
        f"/api/pastes/{slug}/unlock",
        json={"password": "WrongPassword!"},
    )
    assert res5.status_code == 429
    assert "Retry-After" in res5.headers
    assert int(res5.headers["Retry-After"]) > 0
    assert "bloqueado" in res5.json()["detail"].lower()

    # Attempt 6 with CORRECT password must still be rejected with 429
    res6 = await client.post(
        f"/api/pastes/{slug}/unlock",
        json={"password": "MySecretVault99"},
    )
    assert res6.status_code == 429
    assert "Retry-After" in res6.headers


@pytest.mark.asyncio
async def test_tampered_unlock_cookie_rejected(client):
    create_res = await client.post(
        "/api/pastes",
        json={
            "content": "Secret Content",
            "password": "ValidPassword999",
        },
    )
    slug = create_res.json()["slug"]

    # Send bogus cookie
    client.cookies.set(f"inkbin_unlocked_{slug}", "fake_tampered_cookie_val")
    raw_res = await client.get(f"/raw/{slug}")
    assert raw_res.status_code == 401
