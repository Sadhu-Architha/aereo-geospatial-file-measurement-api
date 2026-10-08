from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_zip_upload():
    response = client.post(
        "/api/files/",
        files={
            "file": (
                "invalid.zip",
                b"This is not a shapefile.",
                "application/zip",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid ZIP file"