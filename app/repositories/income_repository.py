from sqlalchemy import extract

from app.models.income import Income


class IncomeRepository:
    @staticmethod
    def list_by_user(user_id, month=None, year=None):
        query = Income.query.filter_by(user_id=user_id)

        if month is not None:
            query = query.filter(extract("month", Income.received_at) == month)
        if year is not None:
            query = query.filter(extract("year", Income.received_at) == year)

        return query.order_by(Income.received_at.desc()).all()

    @staticmethod
    def get_by_id_and_user(income_id, user_id):
        return Income.query.filter_by(id=income_id, user_id=user_id).first()

    @staticmethod
    def create(income):
        from app.extensions import db

        db.session.add(income)
        db.session.commit()
        return income

    @staticmethod
    def delete(income):
        from app.extensions import db

        db.session.delete(income)
        db.session.commit()
