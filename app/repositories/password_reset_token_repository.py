from datetime import datetime, timezone

from app.extensions import db
from app.models.password_reset_token import PasswordResetToken


def utcnow():
    return datetime.now(timezone.utc)


class PasswordResetTokenRepository:
    @staticmethod
    def create(token):
        db.session.add(token)
        db.session.commit()
        return token

    @staticmethod
    def get_valid_by_token_hash(token_hash):
        now = utcnow()
        return PasswordResetToken.query.filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > now,
        ).first()

    @staticmethod
    def invalidate_user_tokens(user_id):
        now = utcnow()
        PasswordResetToken.query.filter(
            PasswordResetToken.user_id == user_id,
            PasswordResetToken.used_at.is_(None),
        ).update({"used_at": now}, synchronize_session=False)
        db.session.commit()

    @staticmethod
    def mark_as_used(token):
        token.used_at = utcnow()
        db.session.commit()
