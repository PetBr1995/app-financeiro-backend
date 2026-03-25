from sqlalchemy import extract

from app.models.expense import Expense


class ExpenseRepository:
    @staticmethod
    def list_by_user(user_id, month=None, year=None):
        query = Expense.query.filter_by(user_id=user_id)

        if month is not None:
            query = query.filter(extract("month", Expense.spent_at) == month)
        if year is not None:
            query = query.filter(extract("year", Expense.spent_at) == year)

        return query.order_by(Expense.spent_at.desc()).all()

    @staticmethod
    def get_by_id_and_user(expense_id, user_id):
        return Expense.query.filter_by(id=expense_id, user_id=user_id).first()

    @staticmethod
    def create(expense):
        from app.extensions import db

        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def delete(expense):
        from app.extensions import db

        db.session.delete(expense)
        db.session.commit()
