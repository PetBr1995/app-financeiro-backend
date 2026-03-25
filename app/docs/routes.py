from flask import Blueprint, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

from app.docs import build_openapi_spec


docs_bp = Blueprint("docs_api", __name__)


@docs_bp.get("/openapi.json")
def openapi_json():
    base_url = request.host_url.rstrip("/")
    return jsonify(build_openapi_spec(base_url=base_url))


def register_swagger_ui(app):
    swaggerui_blueprint = get_swaggerui_blueprint(
        "/docs",
        "/openapi.json",
        config={"app_name": "Financas Pessoais API"},
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix="/docs")
