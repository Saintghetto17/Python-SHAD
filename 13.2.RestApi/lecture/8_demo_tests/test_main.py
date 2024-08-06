from starlette.testclient import TestClient

from main import app

client = TestClient(app)


def test_post_0():
    response = client.get("/posts/0")
    assert response.status_code == 200
    assert response.json() == {"post": {"text": "Hello world!"}}
