import os

from flask import Flask, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-only-change-this-secret-key"
    )

    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        # Some hosted providers still return postgres:// URLs.
        if database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://", "postgresql+psycopg://", 1
            )
        elif database_url.startswith("postgresql://"):
            database_url = database_url.replace(
                "postgresql://", "postgresql+psycopg://", 1
            )
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        # Local development only. Vercel should use DATABASE_URL.
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///expenses.db"
        )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from app.auth.routes import auth_bp
    from app.expenses.routes import expenses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)

    @app.route("/")
    def home():
        if session.get("user_id"):
            return redirect(url_for("expenses.index"))
        return redirect(url_for("auth.login"))

    with app.app_context():
        from app.models import User, Expense  # noqa: F401
        db.create_all()

    return app
