import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_editor_page(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    text = response.text
    assert "INKBIN" in text
    assert "Publicar texto" in text
    assert "paste-content" in text


@pytest.mark.asyncio
async def test_get_new_page(client: AsyncClient):
    response = await client.get("/new")
    assert response.status_code == 200
    assert "INKBIN" in response.text


@pytest.mark.asyncio
async def test_get_static_tokens_css(client: AsyncClient):
    response = await client.get("/static/css/ink-tokens.css")
    assert response.status_code == 200
    assert "--ink-0" in response.text
    assert "--ink-950" in response.text
    assert "--icon-size-sm" in response.text
    assert "--icon-size-md" in response.text
    assert "--icon-size-lg" in response.text
    assert "--icon-stroke" in response.text


@pytest.mark.asyncio
async def test_base_template_includes_tabler_icons(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert "@tabler/icons-webfont" in response.text



@pytest.mark.asyncio
async def test_get_viewer_page_success(client: AsyncClient):
    create_res = await client.post(
        "/api/pastes",
        json={"title": "Código Python Teste", "content": "print('INK')", "language": "python"},
    )
    assert create_res.status_code == 201
    slug = create_res.json()["slug"]

    response = await client.get(f"/p/{slug}")
    assert response.status_code == 200
    assert "Código Python Teste" in response.text
    assert "print(" in response.text
    assert "INK" in response.text
    assert "Copiar código" in response.text


@pytest.mark.asyncio
async def test_get_viewer_page_not_found(client: AsyncClient):
    response = await client.get("/p/notExists")
    assert response.status_code == 404
    assert "Publicação não encontrada" in response.text
