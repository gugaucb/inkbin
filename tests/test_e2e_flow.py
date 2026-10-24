from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from httpx import AsyncClient

from inkbin.models import Paste


@pytest.mark.asyncio
async def test_complete_anonymous_lifecycle_e2e(client: AsyncClient):
    # 1. Post a new paste
    post_payload = {
        "title": "Script de Migração SQL",
        "content": "ALTER TABLE users ADD COLUMN bio TEXT;",
        "language": "sql",
        "expiration": "1d",
    }
    create_res = await client.post("/api/pastes", json=post_payload)
    assert create_res.status_code == 201
    created_data = create_res.json()
    slug = created_data["slug"]
    admin_token = created_data["admin_delete_token"]

    assert len(slug) == 7
    assert len(admin_token) >= 32
    assert "/p/" in created_data["url"]

    # 2. Get via API
    api_res = await client.get(f"/api/pastes/{slug}")
    assert api_res.status_code == 200
    api_data = api_res.json()
    assert api_data["title"] == "Script de Migração SQL"
    assert api_data["content"] == "ALTER TABLE users ADD COLUMN bio TEXT;"
    assert api_data["views_count"] == 1

    # 3. Get raw text
    raw_res = await client.get(f"/raw/{slug}")
    assert raw_res.status_code == 200
    assert raw_res.text == "ALTER TABLE users ADD COLUMN bio TEXT;"
    assert "text/plain" in raw_res.headers["content-type"]

    # 4. Get HTML Viewer
    web_res = await client.get(f"/p/{slug}")
    assert web_res.status_code == 200
    assert "Script de Migração SQL" in web_res.text
    assert "ALTER TABLE users ADD COLUMN bio TEXT;" in web_res.text
    assert "sql" in web_res.text


@pytest.mark.asyncio
async def test_expired_paste_returns_404_everywhere(client: AsyncClient, test_session_factory):
    # Insert an already expired paste directly in the database
    past_time = datetime.now(UTC) - timedelta(hours=2)
    async with test_session_factory() as session:
        expired_paste = Paste(
            slug="exp1234",
            title="Expirado",
            content="secret text",
            language="plaintext",
            admin_delete_hash="hash",
            views_count=0,
            expires_at=past_time,
            created_at=past_time - timedelta(hours=1),
        )
        session.add(expired_paste)
        await session.commit()

    # 1. API GET returns 404
    api_res = await client.get("/api/pastes/exp1234")
    assert api_res.status_code == 404

    # 2. RAW GET returns 404
    raw_res = await client.get("/raw/exp1234")
    assert raw_res.status_code == 404

    # 3. Web UI GET returns 404 template
    web_res = await client.get("/p/exp1234")
    assert web_res.status_code == 404
    assert "Paste not found" in web_res.text or "Publicação não encontrada" in web_res.text


@pytest.mark.asyncio
async def test_sequential_views_increment(client: AsyncClient):
    create_res = await client.post(
        "/api/pastes",
        json={"title": "Contagem", "content": "dados sequenciais"},
    )
    assert create_res.status_code == 201
    slug = create_res.json()["slug"]

    for expected_view in range(1, 6):
        res = await client.get(f"/api/pastes/{slug}")
        assert res.status_code == 200
        assert res.json()["views_count"] == expected_view


def test_frontend_local_history_contract():
    js_file = Path("src/inkbin/static/js/ink-editor.js")
    assert js_file.exists()
    content = js_file.read_text(encoding="utf-8")

    # Verify RF003 contract in frontend script
    assert "inkbin_history" in content
    assert "saveToLocalHistory" in content
    assert "renderHistoryList" in content
    assert "local-history-container" in content
    assert "admin_delete_token" in content
