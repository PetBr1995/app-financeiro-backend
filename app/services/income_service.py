from app.models.income import Income
from app.repositories.income_repository import IncomeRepository
from app.utils.errors import AppError


class IncomeService:
    def __init__(self):
        self.income_repository = IncomeRepository()

    def list_incomes(self, user_id, month=None, year=None):
        return self.income_repository.list_by_user(user_id=user_id, month=month, year=year)

    def create_income(self, user_id, amount, description, received_at):
        income = Income(
            user_id=user_id,
            amount=amount,
            description=description,
            received_at=received_at,
        )
        return self.income_repository.create(income)

    def get_income(self, income_id, user_id):
        income = self.income_repository.get_by_id_and_user(income_id, user_id)
        if not income:
            raise AppError("Receita não encontrada", 404)
        return income

    def update_income(self, income_id, user_id, data):
        income = self.get_income(income_id, user_id)

        from app.extensions import db

        if "amount" in data and data["amount"] is not None:
            income.amount = data["amount"]
        if "description" in data:
            income.description = data["description"]
        if "received_at" in data and data["received_at"] is not None:
            income.received_at = data["received_at"]

        db.session.commit()
        return income

    def delete_income(self, income_id, user_id):
        income = self.get_income(income_id, user_id)
        self.income_repository.delete(income)
