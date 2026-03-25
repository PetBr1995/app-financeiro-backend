from decimal import Decimal

from sqlalchemy import extract, func

from app.extensions import db
from app.models.category import Category
from app.models.expense import Expense
from app.models.income import Income


class DashboardService:
    @staticmethod
    def monthly_summary(user_id, month, year):
        total_incomes = (
            db.session.query(func.coalesce(func.sum(Income.amount), 0))
            .filter(Income.user_id == user_id)
            .filter(extract("month", Income.received_at) == month)
            .filter(extract("year", Income.received_at) == year)
            .scalar()
        )

        total_expenses = (
            db.session.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(Expense.user_id == user_id)
            .filter(extract("month", Expense.spent_at) == month)
            .filter(extract("year", Expense.spent_at) == year)
            .scalar()
        )

        expenses_by_category_rows = (
            db.session.query(Category.name, func.coalesce(func.sum(Expense.amount), 0))
            .join(Expense, Expense.category_id == Category.id)
            .filter(Expense.user_id == user_id)
            .filter(extract("month", Expense.spent_at) == month)
            .filter(extract("year", Expense.spent_at) == year)
            .group_by(Category.name)
            .all()
        )

        expenses_by_category = [
            {"category": name, "total": str(total)} for name, total in expenses_by_category_rows
        ]

        total_incomes = Decimal(total_incomes)
        total_expenses = Decimal(total_expenses)

        return {
            "month": month,
            "year": year,
            "total_incomes": str(total_incomes),
            "total_expenses": str(total_expenses),
            "balance": str(total_incomes - total_expenses),
            "expenses_by_category": expenses_by_category,
        }
