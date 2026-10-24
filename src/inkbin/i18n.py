import json
from pathlib import Path
from typing import Any

from starlette.requests import Request

SUPPORTED_LOCALES = ("en", "pt-br", "cn")
DEFAULT_LOCALE = "en"
COOKIE_NAME = "inkbin_locale"

LOCALES_DIR = Path(__file__).parent / "locales"

_CATALOGS: dict[str, dict[str, str]] = {}


def _flatten_dict(d: dict[str, Any], prefix: str = "") -> dict[str, str]:
    items: dict[str, str] = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.update(_flatten_dict(v, key))
        else:
            items[key] = str(v)
    return items


def load_catalogs(force: bool = False) -> dict[str, dict[str, str]]:
    global _CATALOGS
    if _CATALOGS and not force:
        return _CATALOGS

    catalogs: dict[str, dict[str, str]] = {}
    for loc in SUPPORTED_LOCALES:
        file_path = LOCALES_DIR / f"{loc}.json"
        if file_path.exists():
            try:
                data = json.loads(file_path.read_text(encoding="utf-8"))
                catalogs[loc] = _flatten_dict(data)
            except (json.JSONDecodeError, OSError):
                catalogs[loc] = {}
        else:
            catalogs[loc] = {}

    _CATALOGS = catalogs
    return _CATALOGS


def normalize_locale(locale: str | None) -> str:
    if not locale:
        return DEFAULT_LOCALE

    norm = locale.strip().lower().replace("_", "-")

    if norm in SUPPORTED_LOCALES:
        return norm

    if norm.startswith("pt") or norm in ("pt-br", "pt-pt"):
        return "pt-br"

    if norm.startswith(("zh", "cn")) or norm in ("zh-cn", "zh-hans", "zh-sg", "zh-tw", "zh-hant"):
        return "cn"

    if norm.startswith("en"):
        return "en"

    return DEFAULT_LOCALE


def parse_accept_language(header: str | None) -> str | None:
    if not header:
        return None

    # Parse Accept-Language format: en-US,en;q=0.9,pt-BR;q=0.8
    parts = [p.strip() for p in header.split(",") if p.strip()]
    parsed_entries: list[tuple[float, str]] = []

    for part in parts:
        subparts = [sp.strip() for sp in part.split(";")]
        lang = subparts[0]
        q = 1.0
        for sp in subparts[1:]:
            if sp.startswith("q="):
                try:
                    q = float(sp[2:])
                except ValueError:
                    q = 0.0
        parsed_entries.append((q, lang))

    # Sort descending by quality factor q
    parsed_entries.sort(key=lambda item: item[0], reverse=True)

    for _, lang in parsed_entries:
        candidate = normalize_locale(lang)
        if candidate in SUPPORTED_LOCALES and candidate != DEFAULT_LOCALE:
            return candidate

    return None


def resolve_locale(request: Request) -> str:
    # 1. Query parameter ?lang= or ?locale=
    if request:
        query_lang = request.query_params.get("lang") or request.query_params.get("locale")
        if query_lang:
            return normalize_locale(query_lang)

        # 2. Cookie inkbin_locale
        cookie_lang = request.cookies.get(COOKIE_NAME)
        if cookie_lang:
            return normalize_locale(cookie_lang)

        # 3. Accept-Language HTTP header
        accept_header = request.headers.get("accept-language")
        detected = parse_accept_language(accept_header)
        if detected:
            return detected

    # 4. Fallback to default
    return DEFAULT_LOCALE


def t(key: str, locale: str = DEFAULT_LOCALE, **kwargs: Any) -> str:
    catalogs = load_catalogs()
    loc = normalize_locale(locale)

    text = catalogs.get(loc, {}).get(key)
    if text is None:
        # Fallback to English
        text = catalogs.get(DEFAULT_LOCALE, {}).get(key)

    if text is None:
        # Fallback to key itself
        text = key

    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError, IndexError):
            return text

    return text


def get_client_translations(locale: str) -> dict[str, str]:
    catalogs = load_catalogs()
    loc = normalize_locale(locale)
    return catalogs.get(loc, {})


def i18n_context_processor(request: Request) -> dict[str, Any]:
    from inkbin.expiration import get_expiration_choices

    current_loc = resolve_locale(request)
    return {
        "current_locale": current_loc,
        "t": lambda key, **kwargs: t(key, locale=current_loc, **kwargs),
        "client_i18n_json": json.dumps(get_client_translations(current_loc)),
        "expiration_options": get_expiration_choices(locale=current_loc),
    }
