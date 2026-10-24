import hashlib
from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from inkbin.models import Paste
from inkbin.security import (
    generate_admin_delete_token,
    hash_admin_delete_token,
    hash_password,
)
from inkbin.slug import generate_slug


class SlugCollisionError(RuntimeError):
    """Lançada quando o número máximo de tentativas de resolução de colisão de slug é excedido."""


async def create_paste_record(
    session: AsyncSession,
    title: str | None,
    content: str,
    language: str = "plaintext",
    expires_at: datetime | None = None,
    password: str | None = None,
    content_format: str = "plaintext",
    burn_after_read: bool = False,
    slug_generator: Callable[[], str] = generate_slug,
    max_retries: int = 3,
) -> tuple[Paste, str]:
    """Cria e persiste um Paste com geração segura de slug, retry em colisão e token de admin.

    Retorna uma tupla contendo o modelo Paste persistido e o Admin Delete Token em texto puro.
    """
    admin_token = generate_admin_delete_token()
    admin_hash = hash_admin_delete_token(admin_token)

    is_protected = bool(password)
    password_hash = hash_password(password) if is_protected and password else None
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    for attempt in range(max_retries):
        slug = slug_generator()
        paste = Paste(
            slug=slug,
            title=title,
            content=content,
            language=language,
            admin_delete_hash=admin_hash,
            views_count=0,
            expires_at=expires_at,
            created_at=datetime.now(UTC),
            is_protected=is_protected,
            password_hash=password_hash,
            content_hash=content_hash,
            report_count=0,
            is_active=True,
            content_format=content_format,
            burn_after_read=burn_after_read,
        )

        try:
            # Use begin_nested to allow rollback of the individual insert attempt without aborting the session
            async with session.begin_nested():
                session.add(paste)
                await session.flush()
            await session.commit()
            return paste, admin_token
        except IntegrityError:
            # Rollback savepoint is handled automatically by begin_nested()
            if attempt == max_retries - 1:
                raise SlugCollisionError(
                    f"Falha ao gerar slug único após {max_retries} tentativas."
                )

    raise SlugCollisionError(f"Falha ao gerar slug único após {max_retries} tentativas.")
