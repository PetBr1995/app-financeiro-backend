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


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    # Keep tests isolated and fast regardless of external DATABASE_URL.
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
