from app.api.auth_routes import auth_bp
from app.api.category_routes import category_bp
from app.api.dashboard_routes import dashboard_bp
from app.api.expense_routes import expense_bp
from app.api.income_routes import income_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(income_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(dashboard_bp)
