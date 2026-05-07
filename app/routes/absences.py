from datetime import date

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.extensions import db
from app.models import Absence, Employee


absences_bp = Blueprint("absences", __name__, url_prefix="/employees")


def serialize_absence(absence):
    return {
        "id": absence.id,
        "date": absence.date.isoformat(),
        "created_at": absence.created_at.isoformat(),
        "employee_id": absence.employee_id,
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


@absences_bp.post("/<int:employee_id>/absences")
@jwt_required()
def create_employee_absence(employee_id):
    user_id = int(get_jwt_identity())
    employee = db.session.get(Employee, employee_id)

    if employee is None or employee.user_id != user_id:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    absence_date = data.get("date")

    if absence_date is None:
        return jsonify({"error": "date is required"}), 400

    absence_date, error_response, status_code = parse_date(absence_date, "date")

    if error_response is not None:
        return error_response, status_code

    existing_absence = Absence.query.filter_by(
        employee_id=employee_id,
        date=absence_date
    ).first()

    if existing_absence is not None:
        return jsonify({"error": "Employee already has an absence on this date"}), 409

    absence = Absence(
        employee_id=employee_id,
        date=absence_date,
    )

    try:
        db.session.add(absence)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Employee already has an absence on this date"}), 409
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not create employee absence"}), 500

    return jsonify(serialize_absence(absence)), 201


@absences_bp.get("/<int:employee_id>/absences")
@jwt_required()
def list_employee_absences(employee_id):
    user_id = int(get_jwt_identity())
    employee = db.session.get(Employee, employee_id)

    if employee is None or employee.user_id != user_id:
        return jsonify({"error": "Employee not found"}), 404

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date is not None:
        start_date, error_response, status_code = parse_date(
            start_date,
            "start_date"
        )

        if error_response is not None:
            return error_response, status_code

    if end_date is not None:
        end_date, error_response, status_code = parse_date(end_date, "end_date")

        if error_response is not None:
            return error_response, status_code

    if start_date is not None and end_date is not None and start_date > end_date:
        return jsonify({"error": "start_date cannot be after end_date"}), 400

    query = Absence.query.filter_by(employee_id=employee_id)

    if start_date is not None:
        query = query.filter(Absence.date >= start_date)

    if end_date is not None:
        query = query.filter(Absence.date <= end_date)

    absences = query.order_by(Absence.date.asc()).all()

    return jsonify([serialize_absence(absence) for absence in absences]), 200


@absences_bp.delete("/<int:employee_id>/absences/<int:absence_id>")
@jwt_required()
def delete_employee_absence(employee_id, absence_id):
    user_id = int(get_jwt_identity())
    employee = db.session.get(Employee, employee_id)

    if employee is None or employee.user_id != user_id:
        return jsonify({"error": "Employee not found"}), 404

    absence = db.session.get(Absence, absence_id)

    if absence is None or absence.employee_id != employee_id:
        return jsonify({"error": "Employee absence not found"}), 404

    try:
        db.session.delete(absence)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not delete employee absence"}), 500

    return jsonify({"message": "Employee absence deleted"}), 200
