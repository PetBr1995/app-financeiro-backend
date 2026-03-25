from app.extensions import db
from app.models.user import User


class UserRepository:
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def create(user):
        db.session.add(user)
        db.session.commit()
        return user
