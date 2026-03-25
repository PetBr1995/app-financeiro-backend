from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.dashboard_service import DashboardService
from app.utils.errors import AppError
from app.utils.responses import success_response

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.get("/summary")
@jwt_required()
def monthly_summary():
    user_id = int(get_jwt_identity())

    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)

    now = datetime.utcnow()
    month = month or now.month
    year = year or now.year

    if not (1 <= month <= 12):
        raise AppError("month deve estar entre 1 e 12", 400)
    if year < 1970:
        raise AppError("year inválido", 400)

    data = DashboardService.monthly_summary(user_id=user_id, month=month, year=year)
    return success_response(data=data)
