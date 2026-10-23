import asyncio
import logging
from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from inkbin.cache import CacheService, get_cache_service
from inkbin.models import Paste

logger = logging.getLogger(__name__)


async def purge_expired_pastes(
    session: AsyncSession,
    cache: CacheService | None = None,
) -> int:
    """Executa a varredura assíncrona periódica (sweep runner).

    Remove fisicamente do banco e invalida no Redis todos os pastes com data de expiração vencida.
    Retorna o número de registros expurgados.
    """
    now = datetime.now(UTC)
    stmt = select(Paste.slug).where(Paste.expires_at.is_not(None), Paste.expires_at < now)
    result = await session.execute(stmt)
    expired_slugs = list(result.scalars().all())

    if not expired_slugs:
        return 0

    delete_stmt = delete(Paste).where(Paste.slug.in_(expired_slugs))
    await session.execute(delete_stmt)
    await session.commit()

    if cache is None:
        cache = get_cache_service()

    for slug in expired_slugs:
        await cache.delete(f"paste:{slug}")

    logger.info("Sweep runner: expurgados %d pastes vencidos.", len(expired_slugs))
    return len(expired_slugs)


async def purge_single_expired_paste(
    session: AsyncSession,
    slug: str,
    cache: CacheService | None = None,
) -> None:
    """Expurga on-demand um paste expirado detectado durante a leitura."""
    delete_stmt = delete(Paste).where(Paste.slug == slug)
    await session.execute(delete_stmt)
    await session.commit()

    if cache is None:
        cache = get_cache_service()
    await cache.delete(f"paste:{slug}")


async def run_expiration_sweep_loop(
    interval_seconds: int = 600,
    stop_event: asyncio.Event | None = None,
) -> None:
    """Loop contínuo de background para executar a varredura periódica."""
    from inkbin.db import get_session_maker

    session_factory = get_session_maker()

    while True:
        if stop_event and stop_event.is_set():
            break
        try:
            async with session_factory() as session:
                await purge_expired_pastes(session)
        except Exception as e:  # noqa: BLE001
            logger.error("Erro na execução periódica do sweep runner: %s", e)

        try:
            if stop_event:
                await asyncio.wait_for(stop_event.wait(), timeout=interval_seconds)
                break
            else:
                await asyncio.sleep(interval_seconds)
        except TimeoutError:
            pass
