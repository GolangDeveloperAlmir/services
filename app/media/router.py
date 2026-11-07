"""Read-only, admin-authenticated access to curated local media assets."""

import hashlib
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.auth.dependencies import AdminDep
from app.core.config import settings


router = APIRouter(prefix="/media", tags=["media"])

MAX_MEDIA_BYTES = 15 * 1024 * 1024
MAX_CATALOG_ITEMS = 500
CATEGORIES = ("city", "nature", "ocean", "beach", "anime")
CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".mp3": "audio/mpeg",
    ".ogg": "audio/ogg",
    ".wav": "audio/wav",
}


class MediaItem(BaseModel):
    """Public metadata for one operator-curated, size-bounded media file."""

    id: str
    category: str
    kind: Literal["background", "music"]
    title: str
    content_type: str
    url: str


def _media_files() -> list[tuple[str, str, str, Path]]:
    root = settings.media_root.resolve()
    if not root.is_dir():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Media catalog is unavailable",
        )

    entries: list[tuple[str, str, str, Path]] = []
    for kind, directory in (("background", "backgrounds"), ("music", "music")):
        base = root / directory
        if not base.exists():
            continue
        if base.is_symlink() or not base.is_dir():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Media catalog is unavailable",
            )
        categories = CATEGORIES if kind == "background" else ("ambient",)
        for category in categories:
            category_dir = base / category
            if not category_dir.exists():
                continue
            if category_dir.is_symlink() or not category_dir.is_dir():
                continue
            for candidate in sorted(category_dir.iterdir()):
                if candidate.is_symlink() or not candidate.is_file():
                    continue
                content_type = CONTENT_TYPES.get(candidate.suffix.casefold())
                if content_type is None or candidate.stat().st_size > MAX_MEDIA_BYTES:
                    continue
                try:
                    candidate.resolve().relative_to(root)
                except ValueError:
                    continue
                entries.append((kind, category, content_type, candidate))
                if len(entries) > MAX_CATALOG_ITEMS:
                    raise HTTPException(
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        detail="Media catalog exceeds the configured limit",
                    )
    return entries


def _media_id(path: Path) -> str:
    return hashlib.sha256(
        path.relative_to(settings.media_root.resolve()).as_posix().encode()
    ).hexdigest()[:32]


@router.get("/catalog", response_model=list[MediaItem])
async def media_catalog(_admin: AdminDep) -> list[MediaItem]:
    """List only supported, regular files from the read-only media directory."""
    return [
        MediaItem(
            id=_media_id(path),
            category=category,
            kind=kind,
            title=path.stem[:100],
            content_type=content_type,
            url=f"/media/{_media_id(path)}",
        )
        for kind, category, content_type, path in _media_files()
    ]


@router.get("/{media_id}", response_class=FileResponse)
async def read_media(media_id: str, _admin: AdminDep) -> FileResponse:
    """Stream a catalog item by opaque ID without accepting filesystem paths."""
    if len(media_id) != 32 or any(char not in "0123456789abcdef" for char in media_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    for _kind, _category, content_type, path in _media_files():
        if _media_id(path) == media_id:
            return FileResponse(
                path,
                media_type=content_type,
                filename=f"{media_id}{path.suffix.lower()}",
                content_disposition_type="inline",
                headers={
                    "Cache-Control": "private, no-store",
                    "X-Content-Type-Options": "nosniff",
                    "Content-Security-Policy": "default-src 'none'; sandbox",
                },
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
