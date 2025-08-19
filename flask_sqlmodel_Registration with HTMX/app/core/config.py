from dotenv import load_dotenv

load_dotenv()

import os
from pathlib import Path


class Config:
    # Common configuration settings for the application
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-for-dev-only")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_db_url() -> str:
        env = os.getenv("APP_ENVIRONMENT", "development").lower()

        if env == "production":
            db_url = os.getenv("DATABASE_URL")
            if not db_url:
                raise RuntimeError("❌ DATABASE_URL is required in PRODUCTION environment.")
            return db_url

        elif env == "development":
            db_path = Path(__file__).resolve().parent.parent.parent / "instance" / "app.db"
            return f"sqlite:///{db_path.as_posix()}"

        else:
            raise ValueError(f"❌ Unknown environment: {env}")


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return self.get_db_url()


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return self.get_db_url()
