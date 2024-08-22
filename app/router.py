import os
from typing import Any

from app.database import get_db
from app.services import (
    generate_uid,
    get_media_file,
    save_file,
    save_file_chunked,
    save_metadata,
    upload_to_cloud,
)
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/api/media",
    tags=["Медиа сервис"],
)


@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    uid = generate_uid()

    filename = f"{uid}_{file.filename}"
    file_path = await save_file(file, filename)

    await save_metadata(
        db,
        uid,
        file.filename,
        file_path,
        file.size,
        file.content_type,
        file.filename.split(".")[-1] if file.filename else None,
    )

    await upload_to_cloud(file_path)

    return {"uid": uid, "filename": file.filename}


@router.post("/upload/stream/")
async def upload_file_stream(
    request: Request, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    uid = generate_uid()

    content_disposition = request.headers.get("content-disposition")
    original_name = (
        content_disposition.split("filename=")[-1].replace('"', "")
        if content_disposition
        else "unknown"
    )
    file_format = request.headers.get("content-type", "application/octet-stream")
    extension = original_name.split(".")[-1] if original_name else None

    file_path, file_size = await save_file_chunked(request, uid, original_name)

    await save_metadata(
        db, uid, original_name, file_path, file_size, file_format, extension
    )

    await upload_to_cloud(file_path)

    return {"uid": uid, "filename": original_name}


@router.get("/files/{uid}")
async def get_file(uid: str, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    media_file = await get_media_file(uid, db)
    if not media_file:
        raise HTTPException(status_code=404, detail="File not found")
    return {"file_name": media_file.original_name}
