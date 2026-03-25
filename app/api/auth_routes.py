from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.schemas.auth_schema import LoginSchema, RegisterSchema, UserOutputSchema
from app.services.auth_service import AuthService
from app.utils.responses import success_response

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

register_schema = RegisterSchema()
login_schema = LoginSchema()
user_output_schema = UserOutputSchema()
auth_service = AuthService()


@auth_bp.post("/register")
def register():
    payload = register_schema.load(request.get_json() or {})
    user = auth_service.register(**payload)
    return success_response(
        message="Usuário registrado com sucesso",
        data=user_output_schema.dump(user),
        status_code=201,
    )


@auth_bp.post("/login")
def login():
    payload = login_schema.load(request.get_json() or {})
    token_data = auth_service.login(**payload)
    return success_response(data=token_data)


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = auth_service.get_me(user_id)
    return success_response(data=user_output_schema.dump(user))
