from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models.category import Category
from app.models.user import User

DEFAULT_NAME = "Admin"
DEFAULT_EMAIL = "admin@financas.local"
DEFAULT_PASSWORD = "admin12345"
DEFAULT_CATEGORIES = ["Moradia", "Alimentacao", "Transporte", "Saude", "Lazer"]


def run_seed():
    app = create_app()

    with app.app_context():
        db.create_all()

        user = User.query.filter_by(email=DEFAULT_EMAIL).first()
        if not user:
            user = User(
                name=DEFAULT_NAME,
                email=DEFAULT_EMAIL,
                password_hash=generate_password_hash(DEFAULT_PASSWORD, method="pbkdf2:sha256"),
            )
            db.session.add(user)
            db.session.commit()

        existing_names = {c.name for c in Category.query.filter_by(user_id=user.id).all()}
        for category_name in DEFAULT_CATEGORIES:
            if category_name not in existing_names:
                db.session.add(Category(user_id=user.id, name=category_name))

        db.session.commit()

        print("Seed executada com sucesso.")
        print(f"Email: {DEFAULT_EMAIL}")
        print(f"Senha: {DEFAULT_PASSWORD}")


if __name__ == "__main__":
    run_seed()
