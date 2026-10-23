import asyncio
import logging
import time
from typing import Any

from redis.exceptions import RedisError

logger = logging.getLogger(__name__)


class InMemoryCache:
    """Cache em memória volátil com expiração automática por TTL."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[str, float | None]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> str | None:
        async with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            val, expire_at = entry
            if expire_at is not None and time.monotonic() > expire_at:
                del self._store[key]
                return None
            return val

    async def set(self, key: str, value: str, ttl_seconds: int = 3600) -> None:
        async with self._lock:
            expire_at = time.monotonic() + ttl_seconds if ttl_seconds > 0 else None
            self._store[key] = (value, expire_at)

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._store.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._store.clear()

    async def incr(self, key: str, ttl_seconds: int = 900) -> int:
        async with self._lock:
            now = time.monotonic()
            entry = self._store.get(key)
            if entry is None or (entry[1] is not None and now > entry[1]):
                val = 1
                expire_at = now + ttl_seconds
                self._store[key] = (str(val), expire_at)
                return val
            val = int(entry[0]) + 1
            self._store[key] = (str(val), entry[1])
            return val

    async def ttl(self, key: str) -> int:
        async with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return -2
            expire_at = entry[1]
            if expire_at is None:
                return -1
            remaining = int(expire_at - time.monotonic())
            if remaining <= 0:
                del self._store[key]
                return -2
            return remaining


class CacheService:
    """Serviço unificado de cache com Redis assíncrono e fallback em memória."""

    def __init__(self, redis_url: str | None = None) -> None:
        self.redis_url = redis_url
        self._fallback = InMemoryCache()
        self._redis: Any = None
        if redis_url:
            try:
                import redis.asyncio as aioredis

                self._redis = aioredis.from_url(redis_url, decode_responses=True)
            except (RedisError, OSError) as e:
                logger.warning(
                    "Não foi possível conectar ao Redis (%s). Utilizando fallback em memória.",
                    e,
                )
                self._redis = None

    async def get(self, key: str) -> str | None:
        if self._redis is not None:
            try:
                return await self._redis.get(key)
            except (RedisError, OSError) as e:
                logger.warning(
                    "Erro ao ler do Redis (%s). Consultando fallback em memória.",
                    e,
                )
        return await self._fallback.get(key)

    async def set(self, key: str, value: str, ttl_seconds: int = 3600) -> None:
        if self._redis is not None:
            try:
                await self._redis.set(key, value, ex=ttl_seconds)
                return
            except (RedisError, OSError) as e:
                logger.warning(
                    "Erro ao gravar no Redis (%s). Gravando no fallback em memória.",
                    e,
                )
        await self._fallback.set(key, value, ttl_seconds)

    async def delete(self, key: str) -> None:
        if self._redis is not None:
            try:
                await self._redis.delete(key)
            except (RedisError, OSError) as e:
                logger.warning("Erro ao deletar do Redis (%s).", e)
        await self._fallback.delete(key)

    async def clear(self) -> None:
        if self._redis is not None:
            try:
                await self._redis.flushdb()
            except (RedisError, OSError) as e:
                logger.warning("Erro ao limpar Redis (%s).", e)
        await self._fallback.clear()

    async def incr(self, key: str, ttl_seconds: int = 900) -> int:
        if self._redis is not None:
            try:
                val = await self._redis.incr(key)
                if val == 1:
                    await self._redis.expire(key, ttl_seconds)
                return val
            except (RedisError, OSError) as e:
                logger.warning("Erro ao incrementar no Redis (%s). Usando fallback.", e)
        return await self._fallback.incr(key, ttl_seconds)

    async def ttl(self, key: str) -> int:
        if self._redis is not None:
            try:
                return await self._redis.ttl(key)
            except (RedisError, OSError) as e:
                logger.warning("Erro ao consultar TTL no Redis (%s). Usando fallback.", e)
        return await self._fallback.ttl(key)

    async def close(self) -> None:
        if self._redis is not None:
            try:
                await self._redis.aclose()
            except (RedisError, OSError) as e:
                logger.debug("Erro ao fechar conexão com o Redis (%s).", e)


_cache_instance: CacheService | None = None


def get_cache_service() -> CacheService:
    global _cache_instance
    if _cache_instance is None:
        from inkbin.config import get_settings

        settings = get_settings()
        _cache_instance = CacheService(redis_url=settings.REDIS_URL)
    return _cache_instance
