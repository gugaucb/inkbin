import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_read_aes_gcm_format(client: AsyncClient):
    payload = {
        "title": "AES Test Document",
        "content": "IV12BytesBase64CiphertextAndTag32Bytes",
        "language": "python",
        "expiration": "never",
        "content_format": "aes-256-gcm",
        "burn_after_read": False,
    }
    response = await client.post("/api/pastes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["content_format"] == "aes-256-gcm"
    assert data["burn_after_read"] is False
    slug = data["slug"]

    # Read via API
    get_res = await client.get(f"/api/pastes/{slug}")
    assert get_res.status_code == 200
    detail = get_res.json()
    assert detail["content_format"] == "aes-256-gcm"
    assert detail["content"] == payload["content"]


@pytest.mark.asyncio
async def test_create_and_read_base64_format(client: AsyncClient):
    payload = {
        "title": "Base64 Test Document",
        "content": "SGVsbG8gV29ybGQgZnJvbSBJbmtiaW4h",
        "language": "javascript",
        "expiration": "1d",
        "content_format": "base64",
        "burn_after_read": False,
    }
    response = await client.post("/api/pastes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["content_format"] == "base64"
    assert data["burn_after_read"] is False
    slug = data["slug"]

    get_res = await client.get(f"/api/pastes/{slug}")
    assert get_res.status_code == 200
    detail = get_res.json()
    assert detail["content_format"] == "base64"
    assert detail["content"] == payload["content"]


@pytest.mark.asyncio
async def test_create_paste_rejects_invalid_content_format(client: AsyncClient):
    payload = {
        "title": "Invalid Format",
        "content": "print('hello')",
        "language": "python",
        "content_format": "rot13",
    }
    response = await client.post("/api/pastes", json=payload)
    assert response.status_code == 422
    err_body = response.json()
    assert "content_format" in str(err_body)
