from contextlib import asynccontextmanager

from fastapi import FastAPI

from inkbin.config import get_settings
from inkbin.db import init_db
from inkbin.rate_limit import RateLimitMiddleware
from inkbin.routes.api import router as api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializa tabelas no banco de dados na inicialização
    await init_db()
    yield


app = FastAPI(
    title="Inkbin",
    description="Plataforma editorial para compartilhamento anônimo e seguro de código e textos.",
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    RateLimitMiddleware,
    limit_per_minute=settings.RATE_LIMIT_PER_MINUTE,
)

app.include_router(api_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "app": "inkbin"}
