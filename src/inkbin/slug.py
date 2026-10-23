import secrets

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate_slug(length: int = 7) -> str:
    """Gera um slug criptograficamente aleatório em Base62."""
    if length <= 0:
        raise ValueError("Slug length must be greater than zero")
    return "".join(secrets.choice(BASE62_ALPHABET) for _ in range(length))
