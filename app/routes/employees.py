from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import Employee


employees_bp = Blueprint("employees", __name__, url_prefix="/employees")


def serialize_employee(employee):
    return {
        "id": employee.id,
        "name": employee.name,
        "surname": employee.surname,
        "average_daily_hours": str(employee.average_daily_hours),
        "created_at": employee.created_at.isoformat(),
        "updated_at": employee.updated_at.isoformat(),
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
