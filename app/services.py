import os
import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import aiofiles
from app.config import settings
from app.models import MediaFile
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

UPLOAD_DIR = Path(settings.UPLOAD_DIR)


async def save_file(file, filename: str) -> str:
    file_path = os.path.join(UPLOAD_DIR, filename)
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    return file_path


async def get_media_file(uid: str, db: AsyncSession) -> Optional[MediaFile]:
    result = await db.execute(select(MediaFile).filter(MediaFile.uid == uid))
    return result.scalars().first()


def generate_uid() -> str:
    return str(uuid.uuid4())


async def upload_to_cloud(file_path: str):
    pass


async def save_metadata(
    db: AsyncSession,
    uid: str,
    original_name: str | None,
    file_path: str,
    file_size: int | None,
    file_format: str | None,
    extension: str | None,
) -> Optional[MediaFile]:
    media_file = MediaFile(
        uid=uid,
        original_name=original_name,
        file_path=file_path,
        file_size=file_size,
        file_format=file_format,
        extension=extension,
    )
    db.add(media_file)
    await db.commit()
    await db.refresh(media_file)
    return media_file


async def save_file_chunked(request: Request, uid: str, filename: str) -> str:
    temp_file = NamedTemporaryFile(delete=False, dir=settings.UPLOAD_DIR)
    try:
        async for chunk in request.stream():
            temp_file.write(chunk)

        temp_file.flush()
        temp_file.seek(0, os.SEEK_END)
        file_size = temp_file.tell()
        temp_file.seek(0)

        final_filename = f"{uid}_{filename}"
        final_path = os.path.join(settings.UPLOAD_DIR, final_filename)

        return final_path, file_size
    finally:
        temp_file.close()
        os.rename(temp_file.name, final_path)
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)
