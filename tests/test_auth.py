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


def test_register_password_validation_returns_clear_error(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Bob",
            "email": "bob@example.com",
            "password": "123456",
        },
    )
    body = response.get_json()

    assert response.status_code == 400
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "Dados inválidos"
    assert body["error"]["details"]["password"][0] == "A senha deve ter no mínimo 8 caracteres"


def test_login_invalid_credentials_returns_clear_error(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "nobody@example.com", "password": "wrongpassword"},
    )
    body = response.get_json()

    assert response.status_code == 401
    assert body["error"]["code"] == "app_error"
    assert body["error"]["message"] == "Credenciais inválidas"


def test_me_route_requires_auth(client):
    response = client.get("/api/auth/me")
    body = response.get_json()

    assert response.status_code == 401
    assert body["error"]["code"] == "missing_token"
