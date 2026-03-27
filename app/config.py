import os
from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def _build_cors_origins():
    """
    Resolve allowed CORS origins from env.

    Accepts:
    - "*" (default, useful for local development)
    - Single origin (e.g. https://app.example.com)
    - Comma-separated origins
    """
    raw_origins = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173",
    ).strip()

    if raw_origins == "*":
        return "*"

    origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]
    return origins or "*"


def _build_cors_supports_credentials():
    return os.getenv("CORS_SUPPORTS_CREDENTIALS", "true").strip().lower() == "true"


def _build_password_reset_return_token(default=False):
    return os.getenv("PASSWORD_RESET_RETURN_TOKEN", str(default).lower()).strip().lower() == "true"


def _build_bool_env(name, default=False):
    return os.getenv(name, str(default).lower()).strip().lower() == "true"


def _build_database_uri():
    """
    Resolve a database URI for both local and production environments.

    Rules:
    - If DATABASE_URL exists, use it (production/hosted databases).
    - If DATABASE_URL starts with postgres://, normalize to postgresql://
      for SQLAlchemy compatibility.
    - If DATABASE_URL is not defined, fallback to local SQLite.
    """
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Some platforms still provide postgres://. SQLAlchemy expects postgresql://.
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)

        # Use psycopg v3 driver explicitly (matches requirements: psycopg[binary]).
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

        return database_url

    # Local development fallback (file-based SQLite inside project root).
    return f"sqlite:///{BASE_DIR / 'app.db'}"


def _build_engine_options(database_uri):
    """
    SQLAlchemy engine options tuned for managed Postgres providers.

    pool_pre_ping helps recover stale connections after platform idle periods
    (common in Render/Supabase setups).
    """
    if database_uri.startswith("postgresql://") or database_uri.startswith("postgresql+psycopg://"):
        return {"pool_pre_ping": True}
    return {}


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-with-at-least-32-characters")
    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = _build_engine_options(SQLALCHEMY_DATABASE_URI)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-jwt-secret-key-with-at-least-32-chars")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", "24")))
    CORS_ORIGINS = _build_cors_origins()
    CORS_SUPPORTS_CREDENTIALS = _build_cors_supports_credentials()
    PASSWORD_RESET_TOKEN_EXPIRES_MINUTES = int(os.getenv("PASSWORD_RESET_TOKEN_EXPIRES_MINUTES", "30"))
    PASSWORD_RESET_RETURN_TOKEN = _build_password_reset_return_token(default=False)
    PASSWORD_RESET_FRONTEND_URL = os.getenv(
        "PASSWORD_RESET_FRONTEND_URL",
        "http://localhost:3000/reset-password?token={token}",
    )
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL")
    SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Financas API")
    SMTP_USE_TLS = _build_bool_env("SMTP_USE_TLS", default=True)
    SMTP_USE_SSL = _build_bool_env("SMTP_USE_SSL", default=False)


class DevelopmentConfig(Config):
    DEBUG = True
    PASSWORD_RESET_RETURN_TOKEN = _build_password_reset_return_token(default=True)


class TestingConfig(Config):
    TESTING = True
    # Keep tests isolated and fast regardless of external DATABASE_URL.
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    PASSWORD_RESET_RETURN_TOKEN = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
