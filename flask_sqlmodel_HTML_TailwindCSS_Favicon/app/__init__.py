import os
from flask import Flask, request
from app.core.config import DevelopmentConfig, ProductionConfig
from app.extensions import db, init_extensions
from app.utils.star_generator import generate_svg_stars


def generate_stars():
    path = "app/static/stars/stars.svg"
    if not os.path.exists(path):
        generate_svg_stars(path)


def create_app():
    env = os.getenv("APP_ENVIRONMENT", "development").lower()

    if env == "production":
        config_class = ProductionConfig
    else:
        config_class = DevelopmentConfig

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(DevelopmentConfig())

    if env == "production" and "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
        raise RuntimeError("Production environment must not use SQLite.")

    # Initialize all extensions at once
    init_extensions(app)  # Single initialization call

    # Create tables at startup
    if app.config['DEBUG']:
        with app.app_context():
            db.create_all()

    # Register blueprints here later
    from app.api.users.routes import users
    from app.api.test.routes import tests

    app.register_blueprint(users)
    app.register_blueprint(tests)

    # Generate stars SVG if it doesn't exist
    with app.app_context():
        generate_stars()

    # Cache control for static files
    @app.after_request
    def add_cache_headers(response):
        if request.path.startswith('/static/assets/icons/'):
            response.headers['Cache-Control'] = 'public, max-age=31536000'
        return response

    # just to be sure what is running (mode, database, etc.)
    print(f"\n>>> Running in {env.upper()} mode")
    print(f">>> Using database: {app.config['SQLALCHEMY_DATABASE_URI']}\n")

    return app
