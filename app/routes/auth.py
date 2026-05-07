from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user is not None:
        return jsonify({"error": "Email already registered"}), 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
    )

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already registered"}), 409
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"error": "Could not register user"}), 500

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": access_token}), 200
