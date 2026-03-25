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

## Rodar testes

```bash
pytest -q
```
