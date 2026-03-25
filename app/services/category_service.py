from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.utils.errors import AppError


class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()

    def list_categories(self, user_id):
        return self.category_repository.list_by_user(user_id)

    def create_category(self, user_id, name):
        duplicate = self.category_repository.get_by_name_and_user(name=name, user_id=user_id)
        if duplicate:
            raise AppError("Categoria já existe para este usuário", 409)

        category = Category(user_id=user_id, name=name)
        return self.category_repository.create(category)

    def update_category(self, category_id, user_id, name):
        category = self.category_repository.get_by_id_and_user(category_id, user_id)
        if not category:
            raise AppError("Categoria não encontrada", 404)

        duplicate = self.category_repository.get_by_name_and_user(name=name, user_id=user_id)
        if duplicate and duplicate.id != category.id:
            raise AppError("Categoria já existe para este usuário", 409)

        from app.extensions import db

        category.name = name
        db.session.commit()
        return category

    def delete_category(self, category_id, user_id):
        category = self.category_repository.get_by_id_and_user(category_id, user_id)
        if not category:
            raise AppError("Categoria não encontrada", 404)
        self.category_repository.delete(category)
