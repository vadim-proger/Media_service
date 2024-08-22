from typing import Optional

from pydantic import BaseModel


class MediaFileBase(BaseModel):
    uid: str
    original_name: str
    file_format: str
    file_size: int
    extension: str

    class Config:
        orm_mode = True


class MediaFileCreate(BaseModel):
    original_name: str
    file_format: str
    file_size: int
    extension: str


class MediaFileResponse(MediaFileBase):
    cloud_url: Optional[str] = None
