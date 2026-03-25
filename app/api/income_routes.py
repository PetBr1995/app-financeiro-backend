from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.schemas.income_schema import IncomeCreateSchema, IncomeOutputSchema, IncomeUpdateSchema
from app.services.income_service import IncomeService
from app.utils.errors import AppError
from app.utils.responses import success_response

income_bp = Blueprint("incomes", __name__, url_prefix="/api/incomes")

income_create_schema = IncomeCreateSchema()
income_update_schema = IncomeUpdateSchema()
income_output_schema = IncomeOutputSchema()
income_output_many_schema = IncomeOutputSchema(many=True)
income_service = IncomeService()


def validate_period_filters():
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)

    if "month" in request.args and month is None:
        raise AppError("month deve ser inteiro", 400)
    if "year" in request.args and year is None:
        raise AppError("year deve ser inteiro", 400)
    if month is not None and not (1 <= month <= 12):
        raise AppError("month deve estar entre 1 e 12", 400)
    if year is not None and year < 1970:
        raise AppError("year inválido", 400)

    return month, year


@income_bp.get("")
@jwt_required()
def list_incomes():
    user_id = int(get_jwt_identity())
    month, year = validate_period_filters()
    incomes = income_service.list_incomes(user_id=user_id, month=month, year=year)
    return success_response(data=income_output_many_schema.dump(incomes))


@income_bp.post("")
@jwt_required()
def create_income():
    user_id = int(get_jwt_identity())
    payload = income_create_schema.load(request.get_json() or {})
    income = income_service.create_income(user_id=user_id, **payload)
    return success_response(
        message="Receita criada com sucesso",
        data=income_output_schema.dump(income),
        status_code=201,
    )


@income_bp.get("/<int:income_id>")
@jwt_required()
def get_income(income_id):
    user_id = int(get_jwt_identity())
    income = income_service.get_income(income_id=income_id, user_id=user_id)
    return success_response(data=income_output_schema.dump(income))


@income_bp.put("/<int:income_id>")
@jwt_required()
def update_income(income_id):
    user_id = int(get_jwt_identity())
    payload = income_update_schema.load(request.get_json() or {})
    income = income_service.update_income(income_id=income_id, user_id=user_id, data=payload)
    return success_response(message="Receita atualizada com sucesso", data=income_output_schema.dump(income))


@income_bp.delete("/<int:income_id>")
@jwt_required()
def delete_income(income_id):
    user_id = int(get_jwt_identity())
    income_service.delete_income(income_id=income_id, user_id=user_id)
    return success_response(message="Receita removida com sucesso")
