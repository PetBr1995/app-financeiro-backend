import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    register_payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "strongpass123",
    }
    client.post("/api/auth/register", json=register_payload)

    login_response = client.post(
        "/api/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    token = login_response.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
