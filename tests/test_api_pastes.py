import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_anonymous_paste_success(client: AsyncClient):
    payload = {
        "title": "Configuração NGINX",
        "content": "server { listen 80; }",
        "language": "nginx",
        "expiration": "1d",
    }
    response = await client.post("/api/pastes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "slug" in data
    assert len(data["slug"]) == 7
    assert data["title"] == "Configuração NGINX"
    assert data["language"] == "nginx"
    assert "admin_delete_token" in data
    assert len(data["admin_delete_token"]) >= 32
    assert "url" in data
    assert data["expires_at"] is not None


@pytest.mark.asyncio
async def test_create_paste_validation_empty_content(client: AsyncClient):
    payload = {
        "title": "Vazio",
        "content": "   ",
        "language": "plaintext",
    }
    response = await client.post("/api/pastes", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_paste_exceeding_1mb(client: AsyncClient):
    # 1MB + 10 bytes
    huge_content = "a" * (1024 * 1024 + 10)
    payload = {
        "title": "Grande",
        "content": huge_content,
    }
    response = await client.post("/api/pastes", json=payload)
    assert response.status_code in (413, 422)


@pytest.mark.asyncio
async def test_get_paste_success_and_views_increment(client: AsyncClient):
    create_res = await client.post(
        "/api/pastes",
        json={"title": "Teste Views", "content": "hello world", "language": "python"},
    )
    assert create_res.status_code == 201
    slug = create_res.json()["slug"]

    # First fetch
    get_res1 = await client.get(f"/api/pastes/{slug}")
    assert get_res1.status_code == 200
    data1 = get_res1.json()
    assert data1["content"] == "hello world"
    assert data1["views_count"] == 1

    # Second fetch
    get_res2 = await client.get(f"/api/pastes/{slug}")
    assert get_res2.status_code == 200
    data2 = get_res2.json()
    assert data2["views_count"] == 2


@pytest.mark.asyncio
async def test_get_paste_not_found(client: AsyncClient):
    response = await client.get("/api/pastes/notFoundSlug")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_raw_paste(client: AsyncClient):
    create_res = await client.post(
        "/api/pastes",
        json={"content": "def foo():\n    return 42\n", "language": "python"},
    )
    assert create_res.status_code == 201
    slug = create_res.json()["slug"]

    raw_res = await client.get(f"/raw/{slug}")
    assert raw_res.status_code == 200
    assert "text/plain" in raw_res.headers["content-type"]
    assert raw_res.text == "def foo():\n    return 42\n"


@pytest.mark.asyncio
async def test_create_paste_dynamic_host_url(client: AsyncClient):
    # Test request with Host header of a LAN IP
    headers = {"Host": "192.168.15.8:8000"}
    payload = {
        "title": "LAN Paste",
        "content": "access via LAN IP",
        "language": "plaintext",
    }
    response = await client.post("/api/pastes", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert "192.168.15.8:8000" in data["url"]
    assert data["url"].startswith("http://192.168.15.8:8000/p/")


@pytest.mark.asyncio
async def test_create_paste_reverse_proxy_https_url(client: AsyncClient):
    # Test reverse proxy forwarding headers (Caddy / Let's Encrypt)
    headers = {
        "Host": "paste.example.com",
        "X-Forwarded-Proto": "https",
        "X-Forwarded-Host": "paste.example.com",
    }
    payload = {
        "title": "Secure Paste",
        "content": "secure content behind proxy",
        "language": "plaintext",
    }
    response = await client.post("/api/pastes", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["url"].startswith("https://paste.example.com/p/")
