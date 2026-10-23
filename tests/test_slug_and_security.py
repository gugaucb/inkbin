from inkbin.security import (
    generate_admin_delete_token,
    hash_admin_delete_token,
    verify_admin_delete_token,
)
from inkbin.slug import BASE62_ALPHABET, generate_slug


def test_generate_slug_default_length():
    slug = generate_slug()
    assert len(slug) == 7
    assert all(c in BASE62_ALPHABET for c in slug)


def test_generate_slug_custom_length():
    slug = generate_slug(length=8)
    assert len(slug) == 8
    assert all(c in BASE62_ALPHABET for c in slug)


def test_generate_slug_uniqueness():
    slugs = {generate_slug() for _ in range(100)}
    assert len(slugs) == 100


def test_admin_delete_token_lifecycle():
    token = generate_admin_delete_token()
    assert len(token) >= 32
    token_hash = hash_admin_delete_token(token)
    assert len(token_hash) == 64  # SHA-256 hex string
    assert verify_admin_delete_token(token, token_hash) is True
    assert verify_admin_delete_token("wrong-token", token_hash) is False
