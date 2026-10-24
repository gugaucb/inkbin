import pytest
from starlette.requests import Request
from httpx import AsyncClient, ASGITransport

from inkbin.i18n import (
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
    normalize_locale,
    resolve_locale,
    t,
    load_catalogs,
    get_client_translations,
)
from inkbin.main import app


def test_normalize_locale():
    assert normalize_locale("en") == "en"
    assert normalize_locale("en-US") == "en"
    assert normalize_locale("pt-BR") == "pt-br"
    assert normalize_locale("pt_BR") == "pt-br"
    assert normalize_locale("pt") == "pt-br"
    assert normalize_locale("cn") == "cn"
    assert normalize_locale("zh-CN") == "cn"
    assert normalize_locale("zh") == "cn"
    assert normalize_locale("es") == "en"
    assert normalize_locale(None) == "en"
    assert normalize_locale("") == "en"


def test_translation_helper():
    load_catalogs()
    assert t("meta.title_default", locale="en") == "Inkbin — Anonymous and Secure Editorial Publishing"
    assert t("meta.title_default", locale="pt-br") == "Inkbin — Publicação Editorial Anônima e Segura"
    assert t("meta.title_default", locale="cn") == "Inkbin — 匿名安全的社论级文本分享平台"

    # Interpolation
    assert t("editor.chars", locale="en", count=100) == "100 characters"
    assert t("editor.chars", locale="pt-br", count=100) == "100 caracteres"
    assert t("editor.chars", locale="cn", count=100) == "100 个字符"

    # Fallback to key if unknown
    assert t("non_existent_key_123", locale="en") == "non_existent_key_123"


def test_client_translations():
    data = get_client_translations("pt-br")
    assert isinstance(data, dict)
    assert "clipboard.copied" in data
    assert data["clipboard.copied"] == "Copiado!"


def test_resolve_locale_hierarchy():
    # 1. Query param takes top precedence
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"cookie", b"inkbin_locale=en"), (b"accept-language", b"zh-CN")],
        "query_string": b"lang=pt-br",
    }
    req = Request(scope)
    assert resolve_locale(req) == "pt-br"

    # 2. Cookie takes precedence over Accept-Language
    scope2 = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"cookie", b"inkbin_locale=cn"), (b"accept-language", b"pt-BR")],
        "query_string": b"",
    }
    req2 = Request(scope2)
    assert resolve_locale(req2) == "cn"

    # 3. Accept-Language header
    scope3 = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"accept-language", b"pt-BR,pt;q=0.9,en-US;q=0.8")],
        "query_string": b"",
    }
    req3 = Request(scope3)
    assert resolve_locale(req3) == "pt-br"

    # 4. Fallback to default
    scope4 = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [],
        "query_string": b"",
    }
    req4 = Request(scope4)
    assert resolve_locale(req4) == DEFAULT_LOCALE


@pytest.mark.asyncio
async def test_set_locale_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Switch to pt-br
        resp = await client.get("/set-locale/pt-br", follow_redirects=False)
        assert resp.status_code in (302, 303, 307)
        cookie = resp.cookies.get("inkbin_locale")
        assert cookie == "pt-br"

        # Switch to cn with referer
        resp2 = await client.get("/set-locale/cn", headers={"referer": "http://test/new"}, follow_redirects=False)
        assert resp2.status_code in (302, 303, 307)
        assert resp2.headers.get("location") == "http://test/new"
        assert resp2.cookies.get("inkbin_locale") == "cn"

        # Invalid locale falls back to en
        resp3 = await client.get("/set-locale/xyz", follow_redirects=False)
        assert resp3.status_code in (302, 303, 307)
        assert resp3.cookies.get("inkbin_locale") == "en"


@pytest.mark.asyncio
async def test_qr_code_modal_translations_and_template():
    load_catalogs(force=True)

    # 1. Assert translations exist for all supported locales
    for loc in ("en", "pt-br", "cn"):
        assert t("modal.qr_code_label", locale=loc) != "modal.qr_code_label"
        assert t("modal.qr_code_hint", locale=loc) != "modal.qr_code_hint"
        assert t("modal.qr_code_aria", locale=loc) != "modal.qr_code_aria"

    # Specific locale strings
    assert "QR Code" in t("modal.qr_code_label", locale="en")
    assert "celular" in t("modal.qr_code_label", locale="pt-br")
    assert "二维码" in t("modal.qr_code_label", locale="cn")

    # 2. Assert editor template renders modal QR code elements
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/")
        assert resp.status_code == 200
        html = resp.text
        assert 'id="modal-qrcode"' in html
        assert 'class="qr-code-box"' in html
        assert 'qrcode.min.js' in html
        assert 'role="img"' in html
        assert 'ti ti-qrcode' in html


def test_platform_features_showcase_translations():
    load_catalogs(force=True)

    expected_feature_keys = [
        "features.heading",
        "features.anonymous",
        "features.anonymous_desc",
        "features.encryption",
        "features.encryption_desc",
        "features.expiry",
        "features.expiry_desc",
        "features.developer",
        "features.developer_desc",
        "features.privacy",
        "features.privacy_desc",
        "features.syntax",
        "features.syntax_desc",
        "features.no_signup",
        "features.no_signup_desc",
        "features.delete_token",
        "features.delete_token_desc",
    ]

    for locale in SUPPORTED_LOCALES:
        for key in expected_feature_keys:
            val = t(key, locale=locale)
            assert val != key, f"Missing translation for key '{key}' in locale '{locale}'"
            assert len(val.strip()) > 0, f"Empty translation for key '{key}' in locale '{locale}'"


@pytest.mark.asyncio
async def test_platform_features_showcase_multilingual_rendering():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. English
        resp_en = await client.get("/?lang=en")
        assert resp_en.status_code == 200
        html_en = resp_en.text
        assert "platform-features-section" in html_en
        assert "Platform Guarantees & Features" in html_en
        assert "Anonymous" in html_en
        assert "Encrypted sharing" in html_en
        sec_en = html_en.split('<section class="platform-features-section"')[1].split('</section>')[0]
        assert "features." not in sec_en

        # 2. Portuguese
        resp_pt = await client.get("/?lang=pt-br")
        assert resp_pt.status_code == 200
        html_pt = resp_pt.text
        assert "platform-features-section" in html_pt
        assert "Garantias e Recursos da Plataforma" in html_pt
        assert "Criação anônima" in html_pt
        assert "Compartilhamento protegido" in html_pt
        sec_pt = html_pt.split('<section class="platform-features-section"')[1].split('</section>')[0]
        assert "features." not in sec_pt

        # 3. Chinese
        resp_cn = await client.get("/?lang=cn")
        assert resp_cn.status_code == 200
        html_cn = resp_cn.text
        assert "platform-features-section" in html_cn
        assert "平台保障与特性" in html_cn
        assert "匿名创建" in html_cn
        assert "加密保护" in html_cn
        sec_cn = html_cn.split('<section class="platform-features-section"')[1].split('</section>')[0]
        assert "features." not in sec_cn


def test_security_and_encryption_i18n_keys():
    load_catalogs(force=True)

    required_keys = [
        "editor.format_label",
        "editor.format_plaintext",
        "editor.format_aes_gcm",
        "editor.format_base64",
        "editor.format_base64_hint",
        "editor.burn_label",
        "editor.burn_hint",
        "modal.encrypted_notice",
        "burn.page_title",
        "burn.badge",
        "burn.title",
        "burn.description",
        "burn.confirm_btn",
        "burn.cancel_btn",
        "burn.burned_banner",
        "viewer.base64_badge",
        "viewer.base64_notice",
        "viewer.base64_toggle_decoded",
        "viewer.base64_toggle_raw",
        "viewer.encrypted_badge",
        "viewer.encrypted_missing_key",
        "viewer.encrypted_error",
    ]

    for locale in SUPPORTED_LOCALES:
        for key in required_keys:
            val = t(key, locale=locale)
            assert val != key, f"Missing key '{key}' in locale '{locale}'"
            assert len(val.strip()) > 0, f"Empty key '{key}' in locale '{locale}'"


def test_locale_key_parity():
    catalogs = load_catalogs(force=True)
    en_keys = set(catalogs["en"].keys())
    pt_keys = set(catalogs["pt-br"].keys())
    cn_keys = set(catalogs["cn"].keys())

    missing_in_pt = en_keys - pt_keys
    missing_in_cn = en_keys - cn_keys
    extra_in_pt = pt_keys - en_keys
    extra_in_cn = cn_keys - en_keys

    assert not missing_in_pt, f"Keys missing in pt-br: {missing_in_pt}"
    assert not missing_in_cn, f"Keys missing in cn: {missing_in_cn}"
    assert not extra_in_pt, f"Extra keys in pt-br: {extra_in_pt}"
    assert not extra_in_cn, f"Extra keys in cn: {extra_in_cn}"

