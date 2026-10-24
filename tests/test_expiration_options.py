from datetime import UTC, datetime, timedelta

import pytest

from inkbin.config import get_settings
from inkbin.expiration import (
    calculate_expires_at,
    get_active_expiration_options,
    get_expiration_choices,
    parse_duration_to_seconds,
)


def test_parse_duration_to_seconds():
    assert parse_duration_to_seconds("never") is None
    assert parse_duration_to_seconds("10m") == 600
    assert parse_duration_to_seconds("30m") == 1800
    assert parse_duration_to_seconds("1h") == 3600
    assert parse_duration_to_seconds("12h") == 43200
    assert parse_duration_to_seconds("1d") == 86400
    assert parse_duration_to_seconds("7d") == 604800
    assert parse_duration_to_seconds("1w") == 604800
    assert parse_duration_to_seconds("2w") == 1209600
    assert parse_duration_to_seconds("1m") == 2592000  # 30 days
    assert parse_duration_to_seconds("2mo") == 5184000
    assert parse_duration_to_seconds("3M") == 7776000

    with pytest.raises(ValueError):
        parse_duration_to_seconds("invalid")

    with pytest.raises(ValueError):
        parse_duration_to_seconds("10x")


def test_calculate_expires_at():
    base = datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)
    assert calculate_expires_at("never", base_time=base) is None

    exp_1h = calculate_expires_at("1h", base_time=base)
    assert exp_1h == base + timedelta(hours=1)

    exp_1d = calculate_expires_at("1d", base_time=base)
    assert exp_1d == base + timedelta(days=1)


def test_get_active_expiration_options():
    options = get_active_expiration_options("1h, 1d, never")
    assert options == ["1h", "1d", "never"]

    default_opts = get_active_expiration_options()
    assert "1h" in default_opts
    assert "never" in default_opts


def test_get_expiration_choices():
    choices_en = get_expiration_choices(locale="en")
    assert any(c["value"] == "never" and c["label"] == "Never expire" for c in choices_en)
    assert any(c["value"] == "1h" and c["label"] == "1 hour" for c in choices_en)

    choices_pt = get_expiration_choices(locale="pt-br")
    assert any(c["value"] == "never" and c["label"] == "Nunca expirar" for c in choices_pt)
    assert any(c["value"] == "1h" and c["label"] == "1 hora" for c in choices_pt)


@pytest.mark.asyncio
async def test_api_expiration_validation(monkeypatch, client):
    settings = get_settings()
    monkeypatch.setattr(settings, "EXPIRATION_OPTIONS", "1h,1d,never")

    # Allowed option
    res_ok = await client.post(
        "/api/pastes",
        json={"content": "Valid expiration test", "expiration": "1h"},
    )
    assert res_ok.status_code == 201

    # Disallowed option (1w not in 1h,1d,never)
    res_invalid = await client.post(
        "/api/pastes",
        json={"content": "Invalid expiration test", "expiration": "1w"},
    )
    assert res_invalid.status_code == 422

    # Completely invalid format
    res_bogus = await client.post(
        "/api/pastes",
        json={"content": "Bogus expiration test", "expiration": "invalid_duration"},
    )
    assert res_bogus.status_code == 422

    # Default fallback when expiration is omitted
    res_omitted = await client.post(
        "/api/pastes",
        json={"content": "Omitted expiration test"},
    )
    assert res_omitted.status_code == 201
    data = res_omitted.json()
    assert data["slug"]
