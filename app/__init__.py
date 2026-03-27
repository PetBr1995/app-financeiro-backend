import os

from dotenv import load_dotenv
from flask import Flask
from marshmallow import ValidationError

from app.api import register_blueprints
from app.docs.routes import docs_bp, register_swagger_ui
from app.extensions import init_extensions
from app.utils.errors import AppError
from app.utils.responses import error_response


def create_app(config_name=None):
    load_dotenv()
    # Import config after loading .env so DATABASE_URL and other vars are resolved correctly.
    from app.config import config_by_name

    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    from app import models  # noqa: F401

    init_extensions(app)
    register_blueprints(app)
    app.register_blueprint(docs_bp)
    register_swagger_ui(app)
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return error_response(
            message="Dados inválidos",
            status_code=400,
            code="validation_error",
            details=err.messages,
        )

    @app.errorhandler(AppError)
    def handle_app_error(err):
        return error_response(
            message=err.message,
            status_code=err.status_code,
            code=err.code,
            details=err.details,
        )

    @app.errorhandler(404)
    def handle_not_found(_):
        return error_response("Recurso não encontrado", 404, code="not_found")

    @app.errorhandler(500)
    def handle_internal_error(_):
        return error_response("Erro interno do servidor", 500, code="internal_error")
