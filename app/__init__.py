from flask import Flask
from .config import Config
from .extensions import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models
    from app.routes.absences import absences_bp
    from app.routes.employees import employees_bp

    app.register_blueprint(absences_bp)
    app.register_blueprint(employees_bp)

    @app.route("/")
    def home():
        return {"message": "FairTip API running"}

    return app
