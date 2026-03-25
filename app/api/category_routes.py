from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.schemas.category_schema import CategoryCreateSchema, CategoryOutputSchema, CategoryUpdateSchema
from app.services.category_service import CategoryService
from app.utils.responses import success_response

category_bp = Blueprint("categories", __name__, url_prefix="/api/categories")

category_create_schema = CategoryCreateSchema()
category_update_schema = CategoryUpdateSchema()
category_output_schema = CategoryOutputSchema()
category_output_many_schema = CategoryOutputSchema(many=True)
category_service = CategoryService()


@category_bp.get("")
@jwt_required()
def list_categories():
    user_id = int(get_jwt_identity())
    categories = category_service.list_categories(user_id)
    return success_response(data=category_output_many_schema.dump(categories))


@category_bp.post("")
@jwt_required()
def create_category():
    user_id = int(get_jwt_identity())
    payload = category_create_schema.load(request.get_json() or {})
    category = category_service.create_category(user_id=user_id, name=payload["name"])
    return success_response(
        message="Categoria criada com sucesso",
        data=category_output_schema.dump(category),
        status_code=201,
    )


@category_bp.put("/<int:category_id>")
@jwt_required()
def update_category(category_id):
    user_id = int(get_jwt_identity())
    payload = category_update_schema.load(request.get_json() or {})
    category = category_service.update_category(category_id=category_id, user_id=user_id, name=payload["name"])
    return success_response(message="Categoria atualizada com sucesso", data=category_output_schema.dump(category))


@category_bp.delete("/<int:category_id>")
@jwt_required()
def delete_category(category_id):
    user_id = int(get_jwt_identity())
    category_service.delete_category(category_id=category_id, user_id=user_id)
    return success_response(message="Categoria removida com sucesso", status_code=200)
