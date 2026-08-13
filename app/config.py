import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load variables from .env
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'portfolio.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = str(BASE_DIR / "app" / "static" / "uploads")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")