import asyncio
import logging
import time
from typing import Any

from redis.exceptions import RedisError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)


class InMemoryRateLimiter:
    """Rate limiter em memória utilizando janela deslizante de requisições por chave."""

    def __init__(self) -> None:
        self._history: dict[str, list[float]] = {}
        self._lock = asyncio.Lock()

    async def is_allowed(
        self, key: str, limit: int, window_seconds: int = 60
    ) -> tuple[bool, int]:
        now = time.monotonic()
        threshold = now - window_seconds

        async with self._lock:
            timestamps = self._history.get(key, [])
            valid_timestamps = [ts for ts in timestamps if ts > threshold]

            if len(valid_timestamps) >= limit:
                oldest = valid_timestamps[0]
                retry_after = max(1, int(oldest + window_seconds - now))
                self._history[key] = valid_timestamps
                return False, retry_after

            valid_timestamps.append(now)
            self._history[key] = valid_timestamps
            return True, 0

    async def reset(self) -> None:
        async with self._lock:
            self._history.clear()


class RateLimiter:
    """Rate limiter com backend Redis e fallback transparente em memória."""

    def __init__(self, redis_url: str | None = None) -> None:
        self.redis_url = redis_url
        self._fallback = InMemoryRateLimiter()
        self._redis: Any = None
        if redis_url:
            try:
                import redis.asyncio as aioredis
                self._redis = aioredis.from_url(redis_url, decode_responses=True)
            except (RedisError, OSError) as e:
                logger.warning(
                    "RateLimiter: falha ao conectar ao Redis (%s). Usando fallback em memória.",
                    e,
                )
                self._redis = None

    async def is_allowed(
        self, key: str, limit: int, window_seconds: int = 60
    ) -> tuple[bool, int]:
        if self._redis is not None:
            try:
                redis_key = f"rate:{key}"
                current = await self._redis.incr(redis_key)
                if current == 1:
                    await self._redis.expire(redis_key, window_seconds)
                if current > limit:
                    ttl = await self._redis.ttl(redis_key)
                    retry_after = max(1, ttl if ttl > 0 else window_seconds)
                    return False, retry_after
                return True, 0
            except (RedisError, OSError) as e:
                logger.warning(
                    "RateLimiter Redis falhou (%s). Usando fallback em memória.",
                    e,
                )
        return await self._fallback.is_allowed(key, limit, window_seconds)


_rate_limiter_instance: RateLimiter | None = None


def get_rate_limiter() -> RateLimiter:
    global _rate_limiter_instance
    if _rate_limiter_instance is None:
        from inkbin.config import get_settings
        settings = get_settings()
        _rate_limiter_instance = RateLimiter(redis_url=settings.REDIS_URL)
    return _rate_limiter_instance


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: Any,
        limiter: RateLimiter | None = None,
        limit_per_minute: int = 100,
    ) -> None:
        super().__init__(app)
        self.limiter = limiter or get_rate_limiter()
        self.limit_per_minute = limit_per_minute

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path
        # Skip internal health checks and static files
        if path.startswith("/static") or path == "/health":
            return await call_next(request)

        # Extract client IP respecting forwarded headers
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        elif request.client:
            client_ip = request.client.host
        else:
            client_ip = "127.0.0.1"

        allowed, retry_after = await self.limiter.is_allowed(
            key=client_ip,
            limit=self.limit_per_minute,
            window_seconds=60,
        )

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too Many Requests. Limite de requisições excedido."},
                headers={"Retry-After": str(retry_after)},
            )

        return await call_next(request)
