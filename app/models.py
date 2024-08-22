from app.database import Base
from sqlalchemy import Column, Integer, String


class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True, nullable=False)
    original_name = Column(String)
    file_path = Column(String, nullable=False)
    file_format = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    extension = Column(String, nullable=False)
