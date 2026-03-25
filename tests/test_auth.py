def test_register_and_login(client):
    register_response = client.post(
        "/api/auth/register",
        json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "password123",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={"email": "alice@example.com", "password": "password123"},
    )
    body = login_response.get_json()

    assert login_response.status_code == 200
    assert "access_token" in body["data"]


def test_me_route_requires_auth(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
