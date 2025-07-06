import os
from flask import Flask
from app.core.config import DevelopmentConfig, ProductionConfig
from app.extensions import db, configure_db
from app.core.config import DevelopmentConfig, ProductionConfig


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

    # just to be sure what is running (mode, database, etc.)
    print(f"\n>>> Running in {env.upper()} mode")
    print(f">>> Using database: {app.config['SQLALCHEMY_DATABASE_URI']}\n")

    configure_db(app)  # Initialize DB and other extensions

    # Create tables at startup
    if app.config['DEBUG']:
        with app.app_context():
            db.create_all()

    # Register blueprints here later
    from app.api.users.routes import users as users_blueprint
    from app.api.test.routes import tests as tests_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(tests_blueprint)

    return app
