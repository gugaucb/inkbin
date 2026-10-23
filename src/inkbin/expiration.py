import re
from datetime import UTC, datetime, timedelta
from typing import Any

from inkbin.config import get_settings
from inkbin.i18n import t

DEFAULT_EXPIRATION_OPTIONS = "1h,1d,1w,1m,never"


def get_active_expiration_options(options_str: str | None = None) -> list[str]:
    if options_str is None:
        settings = get_settings()
        options_str = getattr(settings, "EXPIRATION_OPTIONS", DEFAULT_EXPIRATION_OPTIONS)

    tokens = [tok.strip() for tok in options_str.split(",") if tok.strip()]
    return tokens or ["1h", "1d", "1w", "1m", "never"]


def parse_duration_to_seconds(token: str) -> int | None:
    tok = token.strip()
    if tok == "never":
        return None

    if tok == "1m":
        return 30 * 86400  # 1 month in Inkbin

    match = re.match(r"^(\d+)\s*([a-zA-Z]+)$", tok)
    if not match:
        raise ValueError(f"Formato de prazo de expiração inválido: '{token}'.")

    num = int(match.group(1))
    raw_unit = match.group(2)
    unit = raw_unit.lower()

    if raw_unit == "M" or unit in ("mo", "month", "months"):
        return num * 30 * 86400
    elif unit in ("m", "min", "minute", "minutes"):
        return num * 60
    elif unit in ("h", "hr", "hour", "hours"):
        return num * 3600
    elif unit in ("d", "day", "days"):
        return num * 86400
    elif unit in ("w", "wk", "week", "weeks"):
        return num * 7 * 86400
    else:
        raise ValueError(f"Unidade de tempo não suportada: '{match.group(2)}'.")


def parse_duration_to_timedelta(token: str) -> timedelta | None:
    secs = parse_duration_to_seconds(token)
    if secs is None:
        return None
    return timedelta(seconds=secs)


def calculate_expires_at(token: str, base_time: datetime | None = None) -> datetime | None:
    delta = parse_duration_to_timedelta(token)
    if delta is None:
        return None
    base = base_time or datetime.now(UTC)
    return base + delta


def get_expiration_label(token: str, locale: str = "en") -> str:
    key = f"expiration.{token}"
    translated = t(key, locale=locale)
    if translated != key:
        return translated

    tok = token.strip()
    if tok == "never":
        return t("expiration.never", locale=locale)

    match = re.match(r"^(\d+)\s*([a-zA-Z]+)$", tok)
    if not match:
        return tok

    num = int(match.group(1))
    raw_unit = match.group(2)
    unit = raw_unit.lower()

    if raw_unit == "M" or unit in ("mo", "month", "months"):
        k = "expiration.custom_months_plural" if num > 1 else "expiration.custom_months"
        return t(k, locale=locale, count=num)
    elif unit in ("m", "min", "minute", "minutes"):
        k = "expiration.custom_minutes_plural" if num > 1 else "expiration.custom_minutes"
        return t(k, locale=locale, count=num)
    elif unit in ("h", "hr", "hour", "hours"):
        k = "expiration.custom_hours_plural" if num > 1 else "expiration.custom_hours"
        return t(k, locale=locale, count=num)
    elif unit in ("d", "day", "days"):
        k = "expiration.custom_days_plural" if num > 1 else "expiration.custom_days"
        return t(k, locale=locale, count=num)
    elif unit in ("w", "wk", "week", "weeks"):
        k = "expiration.custom_weeks_plural" if num > 1 else "expiration.custom_weeks"
        return t(k, locale=locale, count=num)

    return tok


def get_expiration_choices(locale: str = "en", options_str: str | None = None) -> list[dict[str, str]]:
    active_tokens = get_active_expiration_options(options_str)
    choices: list[dict[str, str]] = []
    for tok in active_tokens:
        choices.append({
            "value": tok,
            "label": get_expiration_label(tok, locale=locale),
        })
    return choices
