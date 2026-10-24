import pytest


@pytest.mark.asyncio
async def test_admin_delete_authorized_success(client):
    # 1. Create paste
    create_res = await client.post(
        "/api/pastes",
        json={"title": "To be deleted", "content": "Ephemeral data content"},
    )
    assert create_res.status_code == 201
    data = create_res.json()
    slug = data["slug"]
    token = data["admin_delete_token"]
    assert len(token) >= 32

    # 2. Warm up cache with GET
    detail_res = await client.get(f"/api/pastes/{slug}")
    assert detail_res.status_code == 200

    # 3. Delete with valid token
    del_res = await client.delete(
        f"/api/pastes/{slug}",
        headers={"X-Admin-Delete-Token": token},
    )
    assert del_res.status_code == 200
    assert del_res.json()["slug"] == slug

    # 4. Subsequent requests must return 404 everywhere
    assert (await client.get(f"/api/pastes/{slug}")).status_code == 404
    assert (await client.get(f"/raw/{slug}")).status_code == 404
    assert (await client.get(f"/p/{slug}")).status_code == 404


@pytest.mark.asyncio
async def test_admin_delete_invalid_token_returns_403(client):
    create_res = await client.post(
        "/api/pastes",
        json={"content": "Protected from wrong tokens"},
    )
    slug = create_res.json()["slug"]

    # Delete with invalid token
    del_res = await client.delete(
        f"/api/pastes/{slug}",
        headers={"X-Admin-Delete-Token": "completely_wrong_admin_token_value_xyz"},
    )
    assert del_res.status_code == 403
    assert "inválido" in del_res.json()["detail"].lower()

    # Paste must remain intact
    assert (await client.get(f"/api/pastes/{slug}")).status_code == 200


@pytest.mark.asyncio
async def test_admin_delete_missing_token_returns_401(client):
    create_res = await client.post(
        "/api/pastes",
        json={"content": "Protected from missing tokens"},
    )
    slug = create_res.json()["slug"]

    del_res = await client.delete(f"/api/pastes/{slug}")
    assert del_res.status_code in (401, 403)


@pytest.mark.asyncio
async def test_web_delete_confirmation_and_action(client):
    create_res = await client.post(
        "/api/pastes",
        json={"title": "Web Delete Test", "content": "Content to delete via web"},
    )
    slug = create_res.json()["slug"]
    token = create_res.json()["admin_delete_token"]

    # GET /p/{slug}/delete renders confirmation page
    get_res = await client.get(f"/p/{slug}/delete")
    assert get_res.status_code == 200
    assert "delete" in get_res.text.lower() or "excluir" in get_res.text.lower()
    assert (
        "irreversible" in get_res.text.lower()
        or "irreversível" in get_res.text.lower()
        or "irreversivel" in get_res.text.lower()
    )

    # Form POST to /p/{slug}/delete with valid token
    post_res = await client.post(
        f"/p/{slug}/delete",
        data={"token": token},
        follow_redirects=True,
    )
    assert post_res.status_code in (200, 302, 303)

    # Paste is now deleted
    assert (await client.get(f"/p/{slug}")).status_code == 404
