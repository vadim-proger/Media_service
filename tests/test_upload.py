from app.database import get_db
from app.main import app, router
from fastapi.testclient import TestClient

client = TestClient(app)
app.include_router(router)


def test_upload_file_success(mock_db, mock_upload_to_cloud):
    app.dependency_overrides[get_db] = lambda: mock_db

    file_content = b"Hello, this is a test file!"

    response = client.post(
        "/api/media/upload/",
        files={"file": ("testfile.txt", file_content, "text/plain")},
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["filename"] == "testfile.txt"

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_upload_file_no_file(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.post("/api/media/upload/")

    assert response.status_code == 422
