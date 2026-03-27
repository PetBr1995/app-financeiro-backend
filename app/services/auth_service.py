import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from flask import current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.password_reset_token import PasswordResetToken
from app.models.user import User
from app.repositories.password_reset_token_repository import PasswordResetTokenRepository
from app.repositories.user_repository import UserRepository
from app.services.email_service import EmailService
from app.utils.errors import AppError


def utcnow():
    return datetime.now(timezone.utc)


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.password_reset_repository = PasswordResetTokenRepository()
        self.email_service = EmailService()

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

    def request_password_reset(self, email):
        user = self.user_repository.get_by_email(email)
        if not user:
            return None

        self.password_reset_repository.invalidate_user_tokens(user.id)

        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
        expires_minutes = current_app.config["PASSWORD_RESET_TOKEN_EXPIRES_MINUTES"]
        expires_at = utcnow() + timedelta(minutes=expires_minutes)

        reset_token = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.password_reset_repository.create(reset_token)

        email_configured = self.email_service.is_configured()

        if email_configured:
            try:
                self.email_service.send_password_reset_email(
                    to_email=user.email,
                    token=raw_token,
                    expires_in_minutes=expires_minutes,
                )
            except Exception:
                raise AppError(
                    "Não foi possível enviar o email de recuperação no momento. Tente novamente.",
                    500,
                    code="email_delivery_failed",
                )
        elif not current_app.config.get("PASSWORD_RESET_RETURN_TOKEN", False):
            raise AppError(
                "Serviço de email não configurado.",
                500,
                code="email_not_configured",
            )

        if not current_app.config.get("PASSWORD_RESET_RETURN_TOKEN", False):
            return None

        return {"reset_token": raw_token, "expires_in_minutes": expires_minutes}

    def reset_password(self, token, password):
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        reset_token = self.password_reset_repository.get_valid_by_token_hash(token_hash)
        if not reset_token:
            raise AppError(
                "Token de redefinição inválido ou expirado",
                400,
                code="invalid_reset_token",
            )

        user = self.user_repository.get_by_id(reset_token.user_id)
        if not user:
            raise AppError("Usuário não encontrado", 404, code="user_not_found")

        user.password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        self.password_reset_repository.invalidate_user_tokens(user.id)
