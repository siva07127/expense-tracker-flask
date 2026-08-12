import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    # Vercel's deployed filesystem is read-only.
    # /tmp is writable, but should NOT be used for the database.
    if os.environ.get("VERCEL"):
        instance_path = "/tmp/expense_tracker_instance"
    else:
        instance_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "instance")
        )

    app = Flask(
        __name__,
        instance_path=instance_path,
        instance_relative_config=True
    )

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-this"
    )

    # -----------------------------
    # DATABASE
    # -----------------------------

    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # Some PostgreSQL providers return postgres://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://",
                "postgresql+psycopg2://",
                1
            )

        # Convert normal postgresql:// URL
        elif database_url.startswith("postgresql://"):
            database_url = database_url.replace(
                "postgresql://",
                "postgresql+psycopg2://",
                1
            )

        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    else:
        # Local development only
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///" +
            os.path.join(instance_path, "expense_tracker.db")
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # -----------------------------
    # BLUEPRINTS
    # -----------------------------

    from app.auth.routes import auth_bp
    from app.expenses.routes import expenses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)

    # -----------------------------
    # CREATE TABLES
    # -----------------------------

    with app.app_context():
        from app.models import User, Expense

        db.create_all()

    return app