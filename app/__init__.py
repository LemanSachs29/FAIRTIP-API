from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt, migrate


def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={r"/*": {"origins": [
            "http://localhost:5173",
            "http://127.0.0.1:5173"
        ]}},
        supports_credentials=True
    )

    #config
    app.config.from_object(Config)

    #extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    #register blueprints
    from app import models
    from app.routes.absences import absences_bp
    from app.routes.auth import auth_bp
    from app.routes.distributions import distributions_bp
    from app.routes.employees import employees_bp

    
    app.register_blueprint(absences_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(distributions_bp)
    app.register_blueprint(employees_bp)

    @app.route("/")
    def home():
        return {"message": "FairTip API running"}

    return app
