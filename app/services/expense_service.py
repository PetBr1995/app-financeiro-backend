from app.models.expense import Expense
from app.repositories.category_repository import CategoryRepository
from app.repositories.expense_repository import ExpenseRepository
from app.utils.errors import AppError


class ExpenseService:
    def __init__(self):
        self.expense_repository = ExpenseRepository()
        self.category_repository = CategoryRepository()

    def list_expenses(self, user_id, month=None, year=None):
        return self.expense_repository.list_by_user(user_id=user_id, month=month, year=year)

    def create_expense(self, user_id, category_id, amount, description, spent_at):
        category = self.category_repository.get_by_id_and_user(category_id, user_id)
        if not category:
            raise AppError("category_id inválido para este usuário", 400)

        expense = Expense(
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            description=description,
            spent_at=spent_at,
        )
        return self.expense_repository.create(expense)

    def get_expense(self, expense_id, user_id):
        expense = self.expense_repository.get_by_id_and_user(expense_id, user_id)
        if not expense:
            raise AppError("Despesa não encontrada", 404)
        return expense

    def update_expense(self, expense_id, user_id, data):
        expense = self.get_expense(expense_id, user_id)

        from app.extensions import db

        if "category_id" in data and data["category_id"] is not None:
            category = self.category_repository.get_by_id_and_user(data["category_id"], user_id)
            if not category:
                raise AppError("category_id inválido para este usuário", 400)
            expense.category_id = data["category_id"]

        if "amount" in data and data["amount"] is not None:
            expense.amount = data["amount"]
        if "description" in data:
            expense.description = data["description"]
        if "spent_at" in data and data["spent_at"] is not None:
            expense.spent_at = data["spent_at"]

        db.session.commit()
        return expense

    def delete_expense(self, expense_id, user_id):
        expense = self.get_expense(expense_id, user_id)
        self.expense_repository.delete(expense)
