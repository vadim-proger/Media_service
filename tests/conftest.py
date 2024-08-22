from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_db():
    db = AsyncMock(spec=AsyncSession)
    yield db


@pytest.fixture
def mock_upload_to_cloud(monkeypatch):
    async def mock_upload(file_path: str):
        return True

    monkeypatch.setattr("app.services.upload_to_cloud", mock_upload)
