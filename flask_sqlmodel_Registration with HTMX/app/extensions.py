from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool
import os

db = SQLAlchemy()


def configure_db(app):
    #  Initialize the database
    if "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "poolclass": NullPool  # Use NullPool for SQLite to avoid connection issues
        }
    db.init_app(app)


def init_favicon(app):
    """Register favicon route with proper caching headers"""

    def init_favicon(app):
        @app.route('/favicon.ico')
        def serve_favicon():
            return send_from_directory(
                os.path.join(app.root_path, 'static', 'assets', 'icons'),
                'favicon.ico',
                mimetype='image/vnd.microsoft.icon'
            )


# Add this function if missing
def init_extensions(app):
    """Initialize all Flask extensions"""
    configure_db(app)
    init_favicon(app)
