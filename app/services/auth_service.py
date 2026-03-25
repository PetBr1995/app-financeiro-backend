from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.errors import AppError


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()

    def register(self, name, email, password):
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise AppError("Email já cadastrado", 409)

        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password, method="pbkdf2:sha256"),
        )
        return self.user_repository.create(user)

    def login(self, email, password):
        user = self.user_repository.get_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            raise AppError("Credenciais inválidas", 401)

        token = create_access_token(identity=str(user.id))
        return {"access_token": token, "token_type": "Bearer"}

    def get_me(self, user_id):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise AppError("Usuário não encontrado", 404)
        return user
