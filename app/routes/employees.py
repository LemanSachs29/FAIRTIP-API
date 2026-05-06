from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import Employee, EmployeeDayOff


employees_bp = Blueprint("employees", __name__, url_prefix="/employees")
VALID_WEEKDAYS = {
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
}


def serialize_employee(employee):
    return {
        "id": employee.id,
        "name": employee.name,
        "surname": employee.surname,
        "average_daily_hours": str(employee.average_daily_hours),
        "created_at": employee.created_at.isoformat(),
        "updated_at": employee.updated_at.isoformat(),
    }


def serialize_day_off(day_off):
    return {
        "id": day_off.id,
        "employee_id": day_off.employee_id,
        "weekday": day_off.weekday,
    }


@employees_bp.post("")
def create_employee():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    name = data.get("name")
    surname = data.get("surname")
    average_daily_hours = data.get("average_daily_hours")


    if not name or not surname or average_daily_hours is None:
        return jsonify({
            "error": "name, surname and average_daily_hours are required"
        }), 400
    

    try:
        average_daily_hours = Decimal(str(average_daily_hours))
    except (InvalidOperation, ValueError):
        return jsonify({"error": "average_daily_hours must be a number"}), 400
    
    if average_daily_hours <= 0:
        return jsonify({"error": "average_daily_hours must be greater than 0"}), 400

    employee = Employee(
        name=name,
        surname=surname,
        average_daily_hours=average_daily_hours,
    )

    try:
        db.session.add(employee)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not create employee"}), 500

    return jsonify(serialize_employee(employee)), 201


@employees_bp.get("")
def list_employees():
    employees = Employee.query.order_by(Employee.id.asc()).all()
    return jsonify([serialize_employee(employee) for employee in employees]), 200


@employees_bp.get("/<int:employee_id>")
def get_employee(employee_id):
    employee = db.session.get(Employee, employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify(serialize_employee(employee)), 200


@employees_bp.put("/<int:employee_id>")
def update_employee(employee_id):
    employee = db.session.get(Employee, employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    name = data.get("name")
    surname = data.get("surname")
    average_daily_hours = data.get("average_daily_hours")

    if not name or not surname or average_daily_hours is None:
        return jsonify({
            "error": "name, surname and average_daily_hours are required"
        }), 400

    try:
        average_daily_hours = Decimal(str(average_daily_hours))
    except (InvalidOperation, ValueError):
        return jsonify({"error": "average_daily_hours must be a number"}), 400

    if average_daily_hours <= 0:
        return jsonify({
            "error": "average_daily_hours must be greater than 0"
        }), 400

    employee.name = name
    employee.surname = surname
    employee.average_daily_hours = average_daily_hours

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not update employee"}), 500

    return jsonify(serialize_employee(employee)), 200


@employees_bp.delete("/<int:employee_id>")
def delete_employee(employee_id):
    employee = db.session.get(Employee, employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    try:
        db.session.delete(employee)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
        "error": "Could not delete employee. It may be linked to absences, day offs or distributions."
        }), 409

    return jsonify({"message": "Employee deleted"}), 200


@employees_bp.post("/<int:employee_id>/day-offs")
def create_employee_day_off(employee_id):
    employee = db.session.get(Employee, employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    weekday = data.get("weekday")

    if weekday not in VALID_WEEKDAYS:
        return jsonify({"error": "weekday must be a valid weekday"}), 400

    existing_day_off = EmployeeDayOff.query.filter_by(
        employee_id=employee_id,
        weekday=weekday
    ).first()

    if existing_day_off is not None:
        return jsonify({"error": "Employee already has this day off"}), 409

    day_off = EmployeeDayOff(
        employee_id=employee_id,
        weekday=weekday,
    )

    try:
        db.session.add(day_off)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not create employee day off"}), 500

    return jsonify(serialize_day_off(day_off)), 201


@employees_bp.get("/<int:employee_id>/day-offs")
def list_employee_day_offs(employee_id):
    employee = db.session.get(Employee, employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    day_offs = EmployeeDayOff.query.filter_by(
        employee_id=employee_id
    ).order_by(EmployeeDayOff.id.asc()).all()

    return jsonify([serialize_day_off(day_off) for day_off in day_offs]), 200


@employees_bp.delete("/<int:employee_id>/day-offs/<int:day_off_id>")
def delete_employee_day_off(employee_id, day_off_id):
    employee = db.session.get(Employee, employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    day_off = db.session.get(EmployeeDayOff, day_off_id)

    if day_off is None or day_off.employee_id != employee_id:
        return jsonify({"error": "Employee day off not found"}), 404

    try:
        db.session.delete(day_off)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not delete employee day off"}), 500

    return jsonify({"message": "Employee day off deleted"}), 200
