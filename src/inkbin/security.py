import hashlib
import hmac
import secrets
import time

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

_hasher = PasswordHasher()


def generate_admin_delete_token() -> str:
    """Gera um token criptograficamente seguro para exclusão administrativa do paste."""
    return secrets.token_urlsafe(32)


def hash_admin_delete_token(token: str) -> str:
    """Retorna o hash SHA-256 do token para armazenamento seguro."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_admin_delete_token(token: str, expected_hash: str) -> bool:
    """Verifica se o token fornecido confere com o hash esperado de forma segura contra timing attacks."""
    computed_hash = hash_admin_delete_token(token)
    return hmac.compare_digest(computed_hash, expected_hash)


def hash_password(password: str) -> str:
    """Gera hash seguro com Argon2id."""
    return _hasher.hash(password)


def verify_password(hashed: str, password: str) -> bool:
    """Verifica senha contra o hash Argon2id."""
    try:
        return _hasher.verify(hashed, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def create_unlock_token(slug: str, secret_key: str | None = None) -> str:
    """Gera valor de cookie assinado para paste desbloqueado por 24 horas."""
    if secret_key is None:
        from inkbin.config import get_settings

        secret_key = get_settings().SECRET_KEY
    timestamp = str(int(time.time()))
    signature = hmac.new(
        secret_key.encode("utf-8"),
        f"{slug}:{timestamp}".encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"{timestamp}:{signature}"


def verify_unlock_token(token: str, slug: str, secret_key: str | None = None) -> bool:
    """Valida integridade e tempo de validade (24h) do cookie assinado."""
    if not token or ":" not in token:
        return False
    try:
        timestamp_str, signature = token.split(":", 1)
        timestamp = int(timestamp_str)
    except ValueError:
        return False

    now = int(time.time())
    # 24 hours = 86400 seconds
    if now - timestamp > 86400 or timestamp > now + 300:
        return False

    if secret_key is None:
        from inkbin.config import get_settings

        secret_key = get_settings().SECRET_KEY

    expected_sig = hmac.new(
        secret_key.encode("utf-8"),
        f"{slug}:{timestamp_str}".encode(),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(signature, expected_sig)
