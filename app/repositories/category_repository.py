from app.models.category import Category


class CategoryRepository:
    @staticmethod
    def list_by_user(user_id):
        return Category.query.filter_by(user_id=user_id).order_by(Category.name.asc()).all()

    @staticmethod
    def get_by_id_and_user(category_id, user_id):
        return Category.query.filter_by(id=category_id, user_id=user_id).first()

    @staticmethod
    def get_by_name_and_user(name, user_id):
        return Category.query.filter_by(name=name, user_id=user_id).first()

    @staticmethod
    def create(category):
        from app.extensions import db

        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def delete(category):
        from app.extensions import db

        db.session.delete(category)
        db.session.commit()
