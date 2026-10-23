from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import PlainTextResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from inkbin.config import get_settings
from inkbin.db import get_db_session
from inkbin.models import Paste
from inkbin.schemas import PasteCreateRequest, PasteCreateResponse, PasteDetailResponse
from inkbin.services import create_paste_record

router = APIRouter(tags=["pastes"])
settings = get_settings()

DbSession = Annotated[AsyncSession, Depends(get_db_session)]


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
    # Check raw byte size
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
    )

    base = settings.BASE_URL.rstrip("/")
    # If base is localhost and request has host header, prefer actual request base url if appropriate
    url = f"{base}/p/{paste.slug}"

    return PasteCreateResponse(
        slug=paste.slug,
        url=url,
        admin_delete_token=admin_token,
        title=paste.title,
        language=paste.language,
        expires_at=paste.expires_at,
        created_at=paste.created_at,
    )


@router.get(
    "/api/pastes/{slug}",
    response_model=PasteDetailResponse,
)
async def get_paste_endpoint(
    slug: str,
    session: DbSession,
) -> PasteDetailResponse:
    stmt = select(Paste).where(Paste.slug == slug)
    result = await session.execute(stmt)
    paste = result.scalar_one_or_none()

    if paste is None or paste.is_expired():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paste não encontrado ou expirado.",
        )

    # Atomic increment of views_count
    await session.execute(
        update(Paste).where(Paste.id == paste.id).values(views_count=Paste.views_count + 1)
    )
    await session.commit()
    await session.refresh(paste)

    return PasteDetailResponse(
        slug=paste.slug,
        title=paste.title,
        content=paste.content,
        language=paste.language,
        views_count=paste.views_count,
        expires_at=paste.expires_at,
        created_at=paste.created_at,
    )


@router.get(
    "/raw/{slug}",
    response_class=PlainTextResponse,
)
async def get_raw_paste_endpoint(
    slug: str,
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
