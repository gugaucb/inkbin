import pytest

from inkbin.security import hash_password, verify_password


def test_argon2_password_hashing():
    pwd = "super-secret-password-123"
    hashed = hash_password(pwd)
    assert hashed.startswith("$argon2id$")
    assert verify_password(hashed, pwd) is True
    assert verify_password(hashed, "wrong-password") is False


@pytest.mark.asyncio
async def test_create_protected_paste_success(client):
    payload = {
        "title": "Secret Logs",
        "content": "CONFIDENTIAL LOG DATA: API_KEY=xyz",
        "language": "plaintext",
        "password": "mySecurePassword123",
    }
    response = await client.post("/api/pastes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["is_protected"] is True
    assert "password" not in data
    assert "password_hash" not in data
    slug = data["slug"]

    # Raw endpoint must return 401
    raw_res = await client.get(f"/raw/{slug}")
    assert raw_res.status_code == 401
    assert "CONFIDENTIAL" not in raw_res.text

    # API endpoint without cookie must return 401
    api_res = await client.get(f"/api/pastes/{slug}")
    assert api_res.status_code == 401
    assert "CONFIDENTIAL" not in api_res.text

    # Web page must render challenge screen, not the secret content
    web_res = await client.get(f"/p/{slug}")
    assert web_res.status_code == 200
    assert "CONFIDENTIAL" not in web_res.text
    assert "senha" in web_res.text.lower() or "password" in web_res.text.lower()


@pytest.mark.asyncio
async def test_create_protected_paste_validation_limits(client):
    # Too short (< 4 chars)
    res_short = await client.post(
        "/api/pastes",
        json={"content": "Valid content", "password": "abc"},
    )
    assert res_short.status_code == 422

    # Too long (> 50 chars)
    res_long = await client.post(
        "/api/pastes",
        json={"content": "Valid content", "password": "a" * 51},
    )
    assert res_long.status_code == 422


@pytest.mark.asyncio
async def test_create_unprotected_paste_returns_is_protected_false(client):
    res = await client.post(
        "/api/pastes",
        json={"content": "Public paste content", "password": None},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["is_protected"] is False

    # Raw is accessible directly
    slug = data["slug"]
    raw_res = await client.get(f"/raw/{slug}")
    assert raw_res.status_code == 200
    assert raw_res.text == "Public paste content"


@pytest.mark.asyncio
async def test_paste_immutability(client):
    res = await client.post(
        "/api/pastes",
        json={"content": "Immutable content"},
    )
    slug = res.json()["slug"]

    put_res = await client.put(f"/api/pastes/{slug}", json={"content": "Changed"})
    assert put_res.status_code in (404, 405)

    patch_res = await client.patch(f"/api/pastes/{slug}", json={"content": "Changed"})
    assert patch_res.status_code in (404, 405)
