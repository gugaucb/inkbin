import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_editor_page(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    text = response.text
    assert "INKBIN" in text
    assert "Publish paste" in text or "Publicar texto" in text
    assert "paste-content" in text
    # Field labels icons
    assert "ti ti-heading" in text
    assert "ti ti-code" in text
    assert "ti ti-clock" in text
    assert "ti ti-lock" in text
    # Editor stats icons
    assert "ti ti-letter-case" in text
    assert "ti ti-database" in text
    # Submit button icon
    assert "ti ti-upload" in text


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
async def test_sidebar_and_topbar_icons(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    text = response.text
    # Sidebar brand icon
    assert "ti ti-terminal" in text or "ti ti-file-text" in text
    # Nav link icon
    assert "ti ti-plus" in text
    # Footer icon
    assert "ti ti-shield-check" in text


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
    assert "Copy code" in response.text or "Copiar código" in response.text

    # Viewer metadata icons
    assert "ti ti-code" in response.text
    assert "ti ti-calendar" in response.text
    assert "ti ti-eye" in response.text

    # Viewer action buttons icons and accessibility labels
    assert "ti ti-copy" in response.text
    assert "ti ti-file-code" in response.text
    assert "ti ti-plus" in response.text
    assert "ti ti-trash" in response.text
    assert "ti ti-flag" in response.text
    assert ('aria-label="View raw code"' in response.text or 'aria-label="Ver código bruto"' in response.text)
    assert ('aria-label="Create new paste"' in response.text or 'aria-label="Criar nova publicação"' in response.text)
    assert ('aria-label="Delete this paste with your Admin Delete Token"' in response.text or 'aria-label="Excluir este paste"' in response.text)
    assert ('aria-label="Report publication"' in response.text or 'aria-label="Denunciar publicação"' in response.text)


@pytest.mark.asyncio
async def test_get_viewer_page_not_found(client: AsyncClient):
    response = await client.get("/p/notExists")
    assert response.status_code == 404
    assert "Paste not found" in response.text or "Publicação não encontrada" in response.text
    assert "ti ti-file-x" in response.text
    assert "ti ti-plus" in response.text


@pytest.mark.asyncio
async def test_modals_and_special_pages_icons(client: AsyncClient):
    # Success modal in editor
    editor_res = await client.get("/")
    assert editor_res.status_code == 200
    assert "ti ti-circle-check" in editor_res.text
    assert "ti ti-external-link" in editor_res.text

    # Create protected paste for challenge page test and report modal test
    create_res = await client.post(
        "/api/pastes",
        json={"title": "Protegido", "content": "segredo", "password": "senha-segura-123"},
    )
    assert create_res.status_code == 201
    slug = create_res.json()["slug"]

    # Challenge page
    challenge_res = await client.get(f"/p/{slug}")
    assert challenge_res.status_code == 200
    assert "ti ti-lock" in challenge_res.text
    assert "ti ti-lock-open" in challenge_res.text
    assert "ti ti-arrow-left" in challenge_res.text

    # Delete confirmation page
    delete_res = await client.get(f"/p/{slug}/delete")
    assert delete_res.status_code == 200
    assert "ti ti-alert-triangle" in delete_res.text
    assert "ti ti-trash" in delete_res.text
    assert "ti ti-arrow-left" in delete_res.text


@pytest.mark.asyncio
async def test_responsive_viewport_and_drawer(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    text = response.text

    # Viewport meta tag
    assert 'name="viewport"' in text
    assert 'content="width=device-width, initial-scale=1.0"' in text

    # Mobile nav drawer and backdrop
    assert 'id="sidebar-backdrop"' in text
    assert 'class="sidebar-backdrop"' in text
    assert 'id="mobile-nav-toggle"' in text
    assert 'class="mobile-nav-toggle"' in text
    assert 'aria-controls="app-sidebar"' in text
    assert 'id="app-sidebar"' in text
    assert 'id="sidebar-close-btn"' in text
    assert 'class="topbar-left"' in text


@pytest.mark.asyncio
async def test_responsive_editor_form_classes(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    text = response.text

    # Form layout and fields
    assert "editor-layout" in text
    assert "editor-header-fields" in text
    assert "field-language" in text
    assert "field-expiration" in text
    assert "field-password" in text
    assert "editor-container" in text
    assert "editor-toolbar" in text
    assert "editor-stats" in text
    assert "editor-footer-actions" in text
    assert "editor-hint-text" in text
    assert "btn-submit" in text

    # Success modal responsive elements
    assert "modal-input-group" in text
    assert "modal-qr-container" in text
    assert "qr-code-box" in text


@pytest.mark.asyncio
async def test_responsive_viewer_code_containment(client: AsyncClient):
    long_code = "const extremelyLongLine = " + "x" * 250 + ";"
    create_res = await client.post(
        "/api/pastes",
        json={"title": "Wide Code Test", "content": long_code, "language": "javascript"},
    )
    assert create_res.status_code == 201
    slug = create_res.json()["slug"]

    response = await client.get(f"/p/{slug}")
    assert response.status_code == 200
    text = response.text

    # Code container and pre formatting
    assert "code-container" in text
    assert "code-content" in text
    assert "ink-code" in text
    assert long_code in text


@pytest.mark.asyncio
async def test_responsive_tokens_and_editorial_css(client: AsyncClient):
    tokens_res = await client.get("/static/css/ink-tokens.css")
    assert tokens_res.status_code == 200
    assert "--breakpoint-mobile: 639px;" in tokens_res.text
    assert "--breakpoint-tablet: 1023px;" in tokens_res.text
    assert "--breakpoint-desktop: 1439px;" in tokens_res.text
    assert "--topbar-height-mobile: 56px;" in tokens_res.text
    assert "--topbar-height-desktop: 64px;" in tokens_res.text
    assert "--touch-target-min: 44px;" in tokens_res.text

    css_res = await client.get("/static/css/ink-editorial.css")
    assert css_res.status_code == 200
    css_text = css_res.text
    assert "clamp(200px, 36vh, 320px)" in css_text
    assert "clamp(300px, 45vh, 420px)" in css_text
    assert "overflow-x: auto;" in css_text
    assert "-webkit-overflow-scrolling: touch;" in css_text
    assert "aux-card" in css_text
    assert "error-card" in css_text


@pytest.mark.asyncio
async def test_responsive_auxiliary_and_error_pages(client: AsyncClient):
    # 404 Error page
    res_404 = await client.get("/p/non-existing-slug-12345")
    assert res_404.status_code == 404
    assert "error-card" in res_404.text
    assert "error-icon" in res_404.text
    assert "error-title" in res_404.text
    assert "error-message" in res_404.text

    # Create protected paste for challenge and delete confirmation tests
    create_res = await client.post(
        "/api/pastes",
        json={"title": "Aux Test", "content": "protected", "password": "pass-aux-test"},
    )
    assert create_res.status_code == 201
    slug = create_res.json()["slug"]

    # Challenge page
    challenge_res = await client.get(f"/p/{slug}")
    assert challenge_res.status_code == 200
    assert "aux-card" in challenge_res.text
    assert "aux-card-header" in challenge_res.text
    assert "aux-card-actions" in challenge_res.text

    # Delete confirmation page
    delete_res = await client.get(f"/p/{slug}/delete")
    assert delete_res.status_code == 200
    assert "aux-card" in delete_res.text
    assert "aux-card-header" in delete_res.text
    assert "aux-card-actions" in delete_res.text
