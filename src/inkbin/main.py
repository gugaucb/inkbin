from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from inkbin.config import get_settings
from inkbin.db import init_db
from inkbin.i18n import COOKIE_NAME, normalize_locale
from inkbin.rate_limit import RateLimitMiddleware
from inkbin.routes.api import router as api_router
from inkbin.routes.web import router as web_router

settings = get_settings()
static_dir = Path(__file__).parent / "static"


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


@app.middleware("http")
async def locale_cookie_middleware(request: Request, call_next):
    response = await call_next(request)
    lang = request.query_params.get("lang") or request.query_params.get("locale")
    if lang:
        norm = normalize_locale(lang)
        response.set_cookie(
            key=COOKIE_NAME,
            value=norm,
            max_age=31536000,
            path="/",
            samesite="lax",
            httponly=False,
        )
    return response


# Servir arquivos estáticos (CSS, JS, Fontes)
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Rotas de API e Rotas Web
app.include_router(api_router)
app.include_router(web_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "app": "inkbin"}
