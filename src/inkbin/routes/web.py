from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from inkbin.cache import get_cache_service
from inkbin.config import get_settings
from inkbin.db import get_db_session
from inkbin.i18n import (
    COOKIE_NAME,
    i18n_context_processor,
    normalize_locale,
)
from inkbin.lifecycle import purge_single_expired_paste
from inkbin.models import Paste
from inkbin.security import verify_admin_delete_token, verify_unlock_token

templates_path = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(
    directory=str(templates_path),
    context_processors=[i18n_context_processor],
)
settings = get_settings()

router = APIRouter(include_in_schema=False)
DbSession = Annotated[AsyncSession, Depends(get_db_session)]


@router.get("/set-locale/{locale}")
async def set_locale_endpoint(locale: str, request: Request) -> Response:
    norm = normalize_locale(locale)
    referer = request.headers.get("referer") or "/"
    if not referer.startswith("/") and not referer.startswith("http://") and not referer.startswith("https://"):
        referer = "/"
    response = RedirectResponse(url=referer, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key=COOKIE_NAME,
        value=norm,
        max_age=31536000,
        path="/",
        samesite="lax",
        httponly=False,
    )
    return response


def is_paste_unlocked(request: Request, slug: str) -> bool:
    cookie_name = f"inkbin_unlocked_{slug}"
    cookie_val = request.cookies.get(cookie_name)
    if not cookie_val:
        return False
    return verify_unlock_token(cookie_val, slug, settings.SECRET_KEY)


@router.get("/", response_class=HTMLResponse)
@router.get("/new", response_class=HTMLResponse)
async def editor_page(request: Request) -> Response:
    return templates.TemplateResponse(
        request=request,
        name="editor.html",
        context={"active_page": "editor"},
    )


@router.get("/p/{slug}/delete", response_class=HTMLResponse)
@router.get("/{slug:[a-zA-Z0-9]{6,10}}/delete", response_class=HTMLResponse)
async def delete_page(
    slug: str,
    request: Request,
    session: DbSession,
) -> Response:
    stmt = select(Paste).where(Paste.slug == slug)
    result = await session.execute(stmt)
    paste = result.scalar_one_or_none()

    if paste is None or paste.is_expired():
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    token = request.query_params.get("token", "")

    return templates.TemplateResponse(
        request=request,
        name="delete_confirmation.html",
        context={
            "paste": paste,
            "token": token,
            "error": None,
            "active_page": "viewer",
        },
    )


@router.post("/p/{slug}/delete", response_class=HTMLResponse)
@router.post("/{slug:[a-zA-Z0-9]{6,10}}/delete", response_class=HTMLResponse)
async def delete_paste_web(
    slug: str,
    request: Request,
    session: DbSession,
) -> Response:
    form = await request.form()
    token = str(form.get("token", "")).strip()

    stmt = select(Paste).where(Paste.slug == slug)
    result = await session.execute(stmt)
    paste = result.scalar_one_or_none()

    if paste is None or paste.is_expired():
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if not token or not verify_admin_delete_token(token, paste.admin_delete_hash):
        return templates.TemplateResponse(
            request=request,
            name="delete_confirmation.html",
            context={
                "paste": paste,
                "token": token,
                "error": "Token de exclusão administrativa inválido.",
                "active_page": "viewer",
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )

    # Perform hard delete
    await session.execute(delete(Paste).where(Paste.id == paste.id))
    await session.commit()

    # Clear cache
    cache = get_cache_service()
    await cache.delete(f"paste:{slug}")

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/p/{slug}", response_class=HTMLResponse)
@router.get("/{slug:[a-zA-Z0-9]{6,10}}", response_class=HTMLResponse)
async def viewer_page(
    slug: str,
    request: Request,
    session: DbSession,
) -> Response:
    stmt = select(Paste).where(Paste.slug == slug)
    result = await session.execute(stmt)
    paste = result.scalar_one_or_none()

    if paste is None or paste.is_expired():
        if paste is not None and paste.is_expired():
            cache = get_cache_service()
            await purge_single_expired_paste(session, slug, cache)
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if not paste.is_active:
        return templates.TemplateResponse(
            request=request,
            name="451.html",
            context={"paste": paste},
            status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        )

    # Check password challenge
    if paste.is_protected and not is_paste_unlocked(request, slug):
        return templates.TemplateResponse(
            request=request,
            name="password_challenge.html",
            context={
                "paste": paste,
                "active_page": "viewer",
            },
            status_code=status.HTTP_200_OK,
        )

    # Check burn after read interstitial confirmation
    if paste.burn_after_read:
        formatted_date = paste.created_at.strftime("%d/%m/%Y às %H:%M")
        return templates.TemplateResponse(
            request=request,
            name="burn_confirmation.html",
            context={
                "paste": paste,
                "formatted_date": formatted_date,
                "active_page": "viewer",
            },
            status_code=status.HTTP_200_OK,
        )

    # Increment view count
    await session.execute(
        update(Paste).where(Paste.id == paste.id).values(views_count=Paste.views_count + 1)
    )
    await session.commit()
    await session.refresh(paste)

    formatted_date = paste.created_at.strftime("%d/%m/%Y às %H:%M")
    formatted_expires = paste.expires_at.strftime("%d/%m/%Y às %H:%M") if paste.expires_at else None

    return templates.TemplateResponse(
        request=request,
        name="viewer.html",
        context={
            "paste": paste,
            "formatted_date": formatted_date,
            "formatted_expires": formatted_expires,
            "was_burned": False,
            "active_page": "viewer",
        },
    )


@router.post("/p/{slug}/reveal", response_class=HTMLResponse)
@router.post("/{slug:[a-zA-Z0-9]{6,10}}/reveal", response_class=HTMLResponse)
async def reveal_burn_after_read_page(
    slug: str,
    request: Request,
    session: DbSession,
) -> Response:
    stmt = select(Paste).where(Paste.slug == slug)
    result = await session.execute(stmt)
    paste = result.scalar_one_or_none()

    if paste is None or paste.is_expired():
        if paste is not None and paste.is_expired():
            cache = get_cache_service()
            await purge_single_expired_paste(session, slug, cache)
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if not paste.is_active:
        return templates.TemplateResponse(
            request=request,
            name="451.html",
            context={"paste": paste},
            status_code=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        )

    if paste.is_protected and not is_paste_unlocked(request, slug):
        return templates.TemplateResponse(
            request=request,
            name="password_challenge.html",
            context={
                "paste": paste,
                "active_page": "viewer",
            },
            status_code=status.HTTP_200_OK,
        )

    # Capture snapshot before deletion
    class PasteSnapshot:
        pass

    snap = PasteSnapshot()
    snap.slug = paste.slug
    snap.title = paste.title
    snap.content = paste.content
    snap.language = paste.language
    snap.content_format = paste.content_format
    snap.burn_after_read = paste.burn_after_read
    snap.views_count = paste.views_count + 1
    snap.created_at = paste.created_at
    snap.expires_at = paste.expires_at
    snap.is_protected = paste.is_protected

    # Delete permanently from database
    await session.execute(delete(Paste).where(Paste.id == paste.id))
    await session.commit()

    # Invalidate cache
    cache = get_cache_service()
    await cache.delete(f"paste:{slug}")

    formatted_date = snap.created_at.strftime("%d/%m/%Y às %H:%M")
    formatted_expires = snap.expires_at.strftime("%d/%m/%Y às %H:%M") if snap.expires_at else None

    return templates.TemplateResponse(
        request=request,
        name="viewer.html",
        context={
            "paste": snap,
            "formatted_date": formatted_date,
            "formatted_expires": formatted_expires,
            "was_burned": True,
            "active_page": "viewer",
        },
    )

