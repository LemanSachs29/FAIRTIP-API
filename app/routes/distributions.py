from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import Distribution, DistributionEntry
from app.services.distribution_service import calculate_distribution


distributions_bp = Blueprint("distributions", __name__, url_prefix="/distributions")


def serialize_distribution(distribution, entries):
    return {
        "id": distribution.id,
        "start_date": distribution.start_date.isoformat(),
        "end_date": distribution.end_date.isoformat(),
        "total_tip_amount": str(distribution.total_tip_amount),
        "total_computed_hours": str(distribution.total_computed_hours),
        "tip_per_hour": str(distribution.tip_per_hour),
        "total_exact_amount": str(distribution.total_exact_amount),
        "total_rounded_amount": str(distribution.total_rounded_amount),
        "remainder_amount": str(distribution.remainder_amount),
        "created_at": distribution.created_at.isoformat(),
        "entries": entries,
    }


def serialize_distribution_entry(entry):
    return {
        "id": entry.id,
        "employee_id": entry.employee_id,
        "day_off_count": entry.day_off_count,
        "absence_count": entry.absence_count,
        "worked_days": entry.worked_days,
        "computed_hours": str(entry.computed_hours),
        "exact_amount": str(entry.exact_amount),
        "rounded_amount": str(entry.rounded_amount),
        "average_daily_hours_snapshot": str(entry.average_daily_hours_snapshot),
    }


def parse_date(value, field_name):
    if not isinstance(value, str):
        return None, jsonify({"error": f"{field_name} must be YYYY-MM-DD"}), 400

    try:
        parsed_date = date.fromisoformat(value)
    except ValueError:
        return None, jsonify({"error": f"{field_name} must be YYYY-MM-DD"}), 400

    if value != parsed_date.isoformat():
        return None, jsonify({"error": f"{field_name} must be YYYY-MM-DD"}), 400

    return parsed_date, None, None


@distributions_bp.post("")
@jwt_required()
def create_distribution():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    start_date_value = data.get("start_date")
    end_date_value = data.get("end_date")
    total_tip_amount_value = data.get("total_tip_amount")

    if not start_date_value or not end_date_value or total_tip_amount_value is None:
        return jsonify({"error": "start_date, end_date and total_tip_amount are required"}), 400

    start_date, error_response, status_code = parse_date(start_date_value, "start_date")
    if error_response:
        return error_response, status_code

    end_date, error_response, status_code = parse_date(end_date_value, "end_date")
    if error_response:
        return error_response, status_code

    if end_date < start_date:
        return jsonify({"error": "end_date must be greater than or equal to start_date"}), 400

    try:
        total_tip_amount = Decimal(str(total_tip_amount_value))
    except (InvalidOperation, ValueError):
        return jsonify({"error": "total_tip_amount must be a number"}), 400

    if total_tip_amount <= 0:
        return jsonify({"error": "total_tip_amount must be greater than 0"}), 400

    try:
        result = calculate_distribution(
            user_id,
            start_date,
            end_date,
            total_tip_amount,
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    distribution = Distribution(
        user_id=user_id,
        start_date=result["start_date"],
        end_date=result["end_date"],
        total_tip_amount=result["total_tip_amount"],
        total_computed_hours=result["total_computed_hours"],
        tip_per_hour=result["tip_per_hour"],
        total_exact_amount=result["total_exact_amount"],
        total_rounded_amount=result["total_rounded_amount"],
        remainder_amount=result["remainder_amount"],
    )

    try:
        db.session.add(distribution)
        db.session.flush()

        entries = []
        for entry_data in result["entries"]:
            entry = DistributionEntry(
                distribution_id=distribution.id,
                employee_id=entry_data["employee_id"],
                day_off_count=entry_data["day_off_count"],
                absence_count=entry_data["absence_count"],
                worked_days=entry_data["worked_days"],
                computed_hours=entry_data["computed_hours"],
                exact_amount=entry_data["exact_amount"],
                rounded_amount=entry_data["rounded_amount"],
                average_daily_hours_snapshot=entry_data["average_daily_hours_snapshot"],
            )
            db.session.add(entry)
            entries.append(entry)

        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not create distribution"}), 500

    serialized_entries = [serialize_distribution_entry(entry) for entry in entries]
    return jsonify(serialize_distribution(distribution, serialized_entries)), 201
