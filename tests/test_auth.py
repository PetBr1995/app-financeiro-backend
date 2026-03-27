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


def test_forgot_and_reset_password_flow(client):
    register_payload = {
        "name": "Carol",
        "email": "carol@example.com",
        "password": "oldpassword123",
    }
    client.post("/api/auth/register", json=register_payload)

    forgot_response = client.post("/api/auth/forgot-password", json={"email": register_payload["email"]})
    forgot_body = forgot_response.get_json()

    assert forgot_response.status_code == 200
    assert "reset_token" in forgot_body["data"]

    reset_response = client.post(
        "/api/auth/reset-password",
        json={
            "token": forgot_body["data"]["reset_token"],
            "password": "newpassword123",
        },
    )
    assert reset_response.status_code == 200

    old_login_response = client.post(
        "/api/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    assert old_login_response.status_code == 401

    new_login_response = client.post(
        "/api/auth/login",
        json={"email": register_payload["email"], "password": "newpassword123"},
    )
    assert new_login_response.status_code == 200


def test_forgot_password_does_not_expose_user_existence(client):
    response = client.post("/api/auth/forgot-password", json={"email": "notfound@example.com"})
    body = response.get_json()

    assert response.status_code == 200
    assert body["message"] == "Se o email estiver cadastrado, você receberá instruções para redefinir a senha."
    assert "data" not in body


def test_reset_password_invalid_token_returns_clear_error(client):
    response = client.post(
        "/api/auth/reset-password",
        json={
            "token": "invalid-token",
            "password": "validpassword123",
        },
    )
    body = response.get_json()

    assert response.status_code == 400
    assert body["error"]["code"] == "invalid_reset_token"
    assert body["error"]["message"] == "Token de redefinição inválido ou expirado"


def test_reset_password_validation_returns_clear_error(client):
    response = client.post(
        "/api/auth/reset-password",
        json={
            "token": "any-token",
            "password": "123456",
        },
    )
    body = response.get_json()

    assert response.status_code == 400
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["details"]["password"][0] == "A senha deve ter no mínimo 8 caracteres"


def test_forgot_password_sends_email_when_configured(client, monkeypatch):
    from app.services.email_service import EmailService

    register_payload = {
        "name": "Mailer User",
        "email": "mailer@example.com",
        "password": "strongpass123",
    }
    client.post("/api/auth/register", json=register_payload)

    sent = {}

    def fake_send_password_reset_email(to_email, token, expires_in_minutes):
        sent["to_email"] = to_email
        sent["token"] = token
        sent["expires_in_minutes"] = expires_in_minutes

    monkeypatch.setattr(EmailService, "is_configured", staticmethod(lambda: True))
    monkeypatch.setattr(
        EmailService,
        "send_password_reset_email",
        staticmethod(fake_send_password_reset_email),
    )

    response = client.post("/api/auth/forgot-password", json={"email": register_payload["email"]})
    body = response.get_json()

    assert response.status_code == 200
    assert sent["to_email"] == register_payload["email"]
    assert sent["expires_in_minutes"] > 0
    assert sent["token"] == body["data"]["reset_token"]


def test_forgot_password_returns_error_when_email_not_configured_and_no_fallback(client, monkeypatch):
    from app.services.email_service import EmailService

    register_payload = {
        "name": "No Mail User",
        "email": "nomail@example.com",
        "password": "strongpass123",
    }
    client.post("/api/auth/register", json=register_payload)

    monkeypatch.setattr(EmailService, "is_configured", staticmethod(lambda: False))

    client.application.config["PASSWORD_RESET_RETURN_TOKEN"] = False
    response = client.post("/api/auth/forgot-password", json={"email": register_payload["email"]})
    body = response.get_json()

    assert response.status_code == 500
    assert body["error"]["code"] == "email_not_configured"
