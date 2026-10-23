import hashlib
import hmac
import secrets


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
