from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.utils.responses import error_response


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()


def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": app.config.get("CORS_ORIGINS", "*"),
                "supports_credentials": app.config.get("CORS_SUPPORTS_CREDENTIALS", False),
                "allow_headers": ["Content-Type", "Authorization"],
                "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            }
        },
    )

    @jwt.unauthorized_loader
    def handle_missing_token(err_msg):
        return error_response(
            message=err_msg,
            status_code=401,
            code="missing_token",
        )

    @jwt.invalid_token_loader
    def handle_invalid_token(err_msg):
        return error_response(
            message=err_msg,
            status_code=401,
            code="invalid_token",
        )

    @jwt.expired_token_loader
    def handle_expired_token(jwt_header, jwt_payload):
        return error_response(
            message="Token expirado",
            status_code=401,
            code="expired_token",
        )

    @jwt.revoked_token_loader
    def handle_revoked_token(jwt_header, jwt_payload):
        return error_response(
            message="Token revogado",
            status_code=401,
            code="revoked_token",
        )
