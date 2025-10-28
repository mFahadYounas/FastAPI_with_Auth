import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from fastapi.testclient import TestClient
from PIL import Image
import io

client = TestClient(app)


def test_get_profile_pic():
    response = client.get("/profile/picture")
    assert response.status_code == 200
    assert response.headers["content-type"] in {"image/png", "image/jpeg"}
    len_content = len(response.content)
    assert len_content <= 50000 and len_content > 0


def test_post_profile_pic():
    img = Image.new("RGB", (200, 200), color="green")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    file = ("test.png", img_bytes, "image/png")
    response = client.post("/profile/picture", files={"file": file})

    response_body = response.json()

    assert response.status_code == 200
    assert response_body["data"]["message"] == "File upload successful!"
    assert response_body["status"] == 200
    assert response_body["error_msg"] == ""


def test_post_profile_pic_format():
    img = Image.new("RGB", (200, 200), color="green")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    file = ("test.pdf", img_bytes, "application/pdf")
    response = client.post("/profile/picture", files={"file": file})

    response_body = response.json()

    assert response.status_code == 400
    assert "Incorrect file type!" in response_body["detail"]


def test_post_profile_pic_size():
    img = Image.new("RGB", (5000, 5000), color="blue")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    file = ("test.png", img_bytes, "image/png")
    response = client.post("/profile/picture", files={"file": file})

    response_body = response.json()

    assert response.status_code == 400
    assert "File too large!" in response_body["detail"]
