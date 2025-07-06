from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool

db = SQLAlchemy()


def configure_db(app):
    #  Initialize the database
    if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "poolclass": NullPool  # Use NullPool for SQLite to avoid connection issues
        }
    db.init_app(app)

