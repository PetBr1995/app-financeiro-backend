from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.schemas.expense_schema import ExpenseCreateSchema, ExpenseOutputSchema, ExpenseUpdateSchema
from app.services.expense_service import ExpenseService
from app.utils.errors import AppError
from app.utils.responses import success_response

expense_bp = Blueprint("expenses", __name__, url_prefix="/api/expenses")

expense_create_schema = ExpenseCreateSchema()
expense_update_schema = ExpenseUpdateSchema()
expense_output_schema = ExpenseOutputSchema()
expense_output_many_schema = ExpenseOutputSchema(many=True)
expense_service = ExpenseService()


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


@expense_bp.get("")
@jwt_required()
def list_expenses():
    user_id = int(get_jwt_identity())
    month, year = validate_period_filters()
    expenses = expense_service.list_expenses(user_id=user_id, month=month, year=year)
    return success_response(data=expense_output_many_schema.dump(expenses))


@expense_bp.post("")
@jwt_required()
def create_expense():
    user_id = int(get_jwt_identity())
    payload = expense_create_schema.load(request.get_json() or {})
    expense = expense_service.create_expense(user_id=user_id, **payload)
    return success_response(
        message="Despesa criada com sucesso",
        data=expense_output_schema.dump(expense),
        status_code=201,
    )


@expense_bp.get("/<int:expense_id>")
@jwt_required()
def get_expense(expense_id):
    user_id = int(get_jwt_identity())
    expense = expense_service.get_expense(expense_id=expense_id, user_id=user_id)
    return success_response(data=expense_output_schema.dump(expense))


@expense_bp.put("/<int:expense_id>")
@jwt_required()
def update_expense(expense_id):
    user_id = int(get_jwt_identity())
    payload = expense_update_schema.load(request.get_json() or {})
    expense = expense_service.update_expense(expense_id=expense_id, user_id=user_id, data=payload)
    return success_response(message="Despesa atualizada com sucesso", data=expense_output_schema.dump(expense))


@expense_bp.delete("/<int:expense_id>")
@jwt_required()
def delete_expense(expense_id):
    user_id = int(get_jwt_identity())
    expense_service.delete_expense(expense_id=expense_id, user_id=user_id)
    return success_response(message="Despesa removida com sucesso")
