import json
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import PlainTextResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from inkbin.cache import get_cache_service
from inkbin.config import get_settings
from inkbin.db import get_db_session
from inkbin.models import Paste
from inkbin.schemas import (
    PasteCreateRequest,
    PasteCreateResponse,
    PasteDetailResponse,
    PasteUnlockRequest,
    PasteUnlockResponse,
)
from inkbin.security import create_unlock_token, verify_password, verify_unlock_token
from inkbin.services import create_paste_record

router = APIRouter(tags=["pastes"])
settings = get_settings()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


def is_paste_unlocked(request: Request, slug: str) -> bool:
    cookie_name = f"inkbin_unlocked_{slug}"
    cookie_val = request.cookies.get(cookie_name)
    if not cookie_val:
        return False
    return verify_unlock_token(cookie_val, slug, settings.SECRET_KEY)


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "127.0.0.1"


@router.post(
    "/api/pastes",
    response_model=PasteCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_paste_endpoint(
    payload: PasteCreateRequest,
    request: Request,
    session: DbSession,
) -> PasteCreateResponse:
    content_bytes = len(payload.content.encode("utf-8"))
    if content_bytes > settings.MAX_PASTE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Conteúdo excede o limite máximo permitido de {settings.MAX_PASTE_BYTES} bytes.",
        )

    expires_at = payload.expiration.to_datetime()

    paste, admin_token = await create_paste_record(
        session=session,
        title=payload.title,
        content=payload.content,
        language=payload.language,
        expires_at=expires_at,
        password=payload.password,
    )

    base = settings.BASE_URL.rstrip("/")
    url = f"{base}/p/{paste.slug}"

    return PasteCreateResponse(
        slug=paste.slug,
        url=url,
        admin_delete_token=admin_token,
        title=paste.title,
        language=paste.language,
        expires_at=paste.expires_at,
        created_at=paste.created_at,
        is_protected=paste.is_protected,
    )


@router.post(
    "/api/pastes/{slug}/unlock",
    response_model=PasteUnlockResponse,
)
async def unlock_paste_endpoint(
    slug: str,
    payload: PasteUnlockRequest,
    request: Request,
    response: Response,
    session: DbSession,
) -> PasteUnlockResponse:
    cache = get_cache_service()
    client_ip = get_client_ip(request)
    attempts_key = f"auth_attempts:{slug}:{client_ip}"

    current_val = await cache.get(attempts_key)
    current_attempts = int(current_val) if current_val else 0

    if current_attempts >= 5:
        ttl = await cache.ttl(attempts_key)
        retry_after = max(1, ttl if ttl > 0 else 900)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas incorretas. Acesso bloqueado por 15 minutos.",
            headers={"Retry-After": str(retry_after)},
        )

    stmt = select(Paste).where(Paste.slug == slug)
    result = await session.execute(stmt)
    paste = result.scalar_one_or_none()

    if paste is None or paste.is_expired():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paste não encontrado ou expirado.",
        )

    if not paste.is_protected:
        return PasteUnlockResponse(
            message="Paste não é protegido por senha.",
            unlocked=True,
            slug=slug,
        )

    if not paste.password_hash or not verify_password(paste.password_hash, payload.password):
        new_attempts = await cache.incr(attempts_key, ttl_seconds=900)
        if new_attempts >= 5:
            ttl = await cache.ttl(attempts_key)
            retry_after = max(1, ttl if ttl > 0 else 900)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Muitas tentativas incorretas. Acesso bloqueado por 15 minutos.",
                headers={"Retry-After": str(retry_after)},
            )
        remaining = 5 - new_attempts
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Senha incorreta. Você tem mais {remaining} tentativa(s) antes do bloqueio temporário.",
        )

    # Password matches: clear lockout counter
    await cache.delete(attempts_key)

    cookie_val = create_unlock_token(slug, settings.SECRET_KEY)
    cookie_name = f"inkbin_unlocked_{slug}"
    response.set_cookie(
        key=cookie_name,
        value=cookie_val,
        max_age=86400,
        httponly=True,
        samesite="lax",
        secure=settings.APP_ENV == "production",
    )

    return PasteUnlockResponse(
        message="Paste desbloqueado com sucesso.",
        unlocked=True,
        slug=slug,
    )


@router.get(
    "/api/pastes/{slug}",
    response_model=PasteDetailResponse,
)
async def get_paste_endpoint(
    slug: str,
    request: Request,
    session: DbSession,
) -> PasteDetailResponse:
    cache = get_cache_service()
    cache_key = f"paste:{slug}"
    cached = await cache.get(cache_key)

    if cached:
        data = json.loads(cached)
        if data.get("expires_at"):
            exp = datetime.fromisoformat(data["expires_at"])
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=UTC)
            if exp < datetime.now(UTC):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Paste não encontrado ou expirado.",
                )
        if data.get("is_protected", False) and not is_paste_unlocked(request, slug):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Paste protegido por senha. Autenticação necessária.",
            )
        await session.execute(
            update(Paste).where(Paste.slug == slug).values(views_count=Paste.views_count + 1)
        )
        await session.commit()
        data["views_count"] = data.get("views_count", 0) + 1
        await cache.set(cache_key, json.dumps(data), ttl_seconds=3600)
        return PasteDetailResponse(**data)

    stmt = select(Paste).where(Paste.slug == slug)
    result = await session.execute(stmt)
    paste = result.scalar_one_or_none()

    if paste is None or paste.is_expired():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paste não encontrado ou expirado.",
        )

    if paste.is_protected and not is_paste_unlocked(request, slug):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Paste protegido por senha. Autenticação necessária.",
        )

    # Atomic increment of views_count
    await session.execute(
        update(Paste).where(Paste.id == paste.id).values(views_count=Paste.views_count + 1)
    )
    await session.commit()
    await session.refresh(paste)

    response = PasteDetailResponse(
        slug=paste.slug,
        title=paste.title,
        content=paste.content,
        language=paste.language,
        views_count=paste.views_count,
        expires_at=paste.expires_at,
        created_at=paste.created_at,
        is_protected=paste.is_protected,
    )

    ttl = 3600
    if paste.expires_at is not None:
        now = datetime.now(UTC)
        exp = paste.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=UTC)
        remaining = int((exp - now).total_seconds())
        if remaining > 0:
            ttl = min(3600, remaining)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paste não encontrado ou expirado.",
            )

    await cache.set(cache_key, response.model_dump_json(), ttl_seconds=ttl)
    return response


@router.get(
    "/raw/{slug}",
    response_class=PlainTextResponse,
)
async def get_raw_paste_endpoint(
    slug: str,
    request: Request,
    session: DbSession,
) -> Response:
    stmt = select(Paste).where(Paste.slug == slug)
    result = await session.execute(stmt)
    paste = result.scalar_one_or_none()

    if paste is None or paste.is_expired():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paste não encontrado ou expirado.",
        )

    if paste.is_protected and not is_paste_unlocked(request, slug):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Paste protegido por senha. Autenticação necessária.",
        )

    # Atomic increment of views_count
    await session.execute(
        update(Paste).where(Paste.id == paste.id).values(views_count=Paste.views_count + 1)
    )
    await session.commit()

    return PlainTextResponse(
        content=paste.content,
        status_code=200,
        media_type="text/plain; charset=utf-8",
    )
