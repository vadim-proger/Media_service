from app.database import get_db
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_upload_file_stream_success(mock_db, mock_upload_to_cloud):
    app.dependency_overrides[get_db] = lambda: mock_db

    headers = {
        "content-disposition": 'attachment; filename="testfile.txt"',
        "content-type": "text/plain",
    }
    data = b"Hello, this is a test file!"

    response = client.post("/api/media/upload/stream/", data=data, headers=headers)

    assert response.status_code == 200
    assert "uid" in response.json()
    assert response.json()["filename"] == "testfile.txt"


def test_upload_file_stream_missing_content_type(mock_db, mock_upload_to_cloud):
    app.dependency_overrides[get_db] = lambda: mock_db

    headers = {
        "content-disposition": 'attachment; filename="testfile.txt"',
    }
    data = b"Hello, this is a test file!"

    response = client.post("/api/media/upload/stream/", data=data, headers=headers)

    assert response.status_code == 200
    assert "uid" in response.json()
    assert response.json()["filename"] == "testfile.txt"


def test_upload_file_stream_empty_file(mock_db, mock_upload_to_cloud):
    app.dependency_overrides[get_db] = lambda: mock_db

    headers = {
        "content-disposition": 'attachment; filename="emptyfile.txt"',
        "content-type": "text/plain",
    }
    data = b""

    response = client.post("/api/media/upload/stream/", data=data, headers=headers)

    assert response.status_code == 200
    assert "uid" in response.json()
    assert response.json()["filename"] == "emptyfile.txt"
