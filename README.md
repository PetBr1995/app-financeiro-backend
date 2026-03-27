# Backend - SaaS de Finanças Pessoais (MVP)

Backend Flask organizado em camadas para evoluir de uso pessoal para SaaS multiusuário.

## Stack

- Python 3.12+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Flask-Swagger-UI
- SQLite
- Marshmallow
- python-dotenv

## Estrutura

```text
backend/
  app/
    __init__.py
    config.py
    extensions.py
    models/
    repositories/
    services/
    schemas/
    api/
    docs/
    utils/
  migrations/
  tests/
  run.py
  requirements.txt
  .env.example
  README.md
```

## Como rodar localmente

1. Criar ambiente virtual:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

3. Configurar variáveis de ambiente:

```bash
cp .env.example .env
```

4. Executar migrações:

```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "initial schema"
flask db upgrade
```

5. Rodar aplicação:

```bash
flask run
```

API disponível em `http://127.0.0.1:5000`.

## Documentação da API

- Swagger UI: `http://127.0.0.1:5000/docs`
- OpenAPI JSON: `http://127.0.0.1:5000/openapi.json`

### Como importar no Postman

1. Abrir Postman.
2. Clicar em **Import**.
3. Escolher **Link**.
4. Colar: `http://127.0.0.1:5000/openapi.json`.
5. Importar.

## Endpoints

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/forgot-password`
- `POST /api/auth/reset-password`
- `GET /api/auth/me`

### Categories
- `GET /api/categories`
- `POST /api/categories`
- `PUT /api/categories/<id>`
- `DELETE /api/categories/<id>`

### Incomes
- `GET /api/incomes`
- `POST /api/incomes`
- `GET /api/incomes/<id>`
- `PUT /api/incomes/<id>`
- `DELETE /api/incomes/<id>`

### Expenses
- `GET /api/expenses`
- `POST /api/expenses`
- `GET /api/expenses/<id>`
- `PUT /api/expenses/<id>`
- `DELETE /api/expenses/<id>`

### Dashboard
- `GET /api/dashboard/summary?month=3&year=2026`

## Integração Frontend (Auth)

### Formato padrão de erro

```json
{
  "error": {
    "code": "validation_error",
    "message": "Dados inválidos",
    "details": {
      "password": ["A senha deve ter no mínimo 8 caracteres"]
    }
  }
}
```

### Recuperar senha

`POST /api/auth/forgot-password`

Request:

```json
{
  "email": "user@example.com"
}
```

Response (`200`):

```json
{
  "message": "Se o email estiver cadastrado, você receberá instruções para redefinir a senha."
}
```

Observação:
- Em `development/testing`, pode retornar `data.reset_token` para facilitar testes de frontend.
- Em `production`, o recomendado é não retornar token na API (`PASSWORD_RESET_RETURN_TOKEN=false`).
- Com SMTP configurado, o backend envia email real com link de redefinição.

### Redefinir senha

`POST /api/auth/reset-password`

Request:

```json
{
  "token": "TOKEN_DE_RECUPERACAO",
  "password": "novaSenha123"
}
```

Response (`200`):

```json
{
  "message": "Senha redefinida com sucesso"
}
```

Erros esperados:
- `400 validation_error` para senha inválida (ex.: menos de 8 caracteres).
- `400 invalid_reset_token` para token inválido, expirado ou já utilizado.

### Variáveis para envio de email

- `PASSWORD_RESET_FRONTEND_URL` (ex.: `https://seu-front.com/reset-password?token={token}`)
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_FROM_EMAIL`
- `SMTP_FROM_NAME`
- `SMTP_USE_TLS`
- `SMTP_USE_SSL`

## Rodar testes

```bash
pytest -q
```
