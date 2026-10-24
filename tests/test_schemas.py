from datetime import UTC, datetime
import pytest
from pydantic import ValidationError

from inkbin.schemas import (
    PasteCreateRequest,
    PasteCreateResponse,
    PasteDetailResponse,
)


def test_paste_create_request_content_format_defaults():
    req = PasteCreateRequest(
        content="Hello world",
    )
    assert req.content_format == "plaintext"
    assert req.burn_after_read is False


def test_paste_create_request_valid_content_formats():
    for fmt in ["plaintext", "aes-256-gcm", "base64"]:
        req = PasteCreateRequest(content="hello", content_format=fmt, burn_after_read=True)
        assert req.content_format == fmt
        assert req.burn_after_read is True


def test_paste_create_request_invalid_content_format():
    with pytest.raises(ValidationError) as exc_info:
        PasteCreateRequest(content="hello", content_format="invalid-format")
    assert "content_format" in str(exc_info.value)


def test_paste_responses_include_new_fields():
    create_resp = PasteCreateResponse(
        slug="abc1234",
        url="http://localhost:8000/p/abc1234",
        admin_delete_token="token123",
        title="Title",
        language="python",
        expires_at=None,
        created_at=datetime.now(UTC),
        is_protected=False,
        content_format="aes-256-gcm",
        burn_after_read=True,
    )
    assert create_resp.content_format == "aes-256-gcm"
    assert create_resp.burn_after_read is True

    detail_resp = PasteDetailResponse(
        slug="abc1234",
        title="Title",
        content="secret",
        language="python",
        views_count=1,
        expires_at=None,
        created_at=datetime.now(UTC),
        is_protected=False,
        is_active=True,
        content_format="base64",
        burn_after_read=False,
    )
    assert detail_resp.content_format == "base64"
    assert detail_resp.burn_after_read is False
