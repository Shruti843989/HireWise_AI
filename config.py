import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory of the Project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file if it exists
load_dotenv(BASE_DIR / ".env")

class Config:
    BASE_DIR = BASE_DIR
    # Flask Settings
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "hirewise_secure_fallback_secret_key_2026")
    ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = ENV == "development"

    # Database Settings
    # Store SQLite db relative to BASE_DIR if relative path is provided
    db_url = os.environ.get("DATABASE_URL", "sqlite:///database/hirewise.db")
    if db_url.startswith("sqlite:///"):
        # Make sure database directory is fully resolved
        db_path = db_url.replace("sqlite:///", "")
        db_abs_path = BASE_DIR / db_path
        # Ensure parent directory of DB exists
        db_abs_path.parent.mkdir(parents=True, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_abs_path.resolve()}"
    else:
        SQLALCHEMY_DATABASE_URI = db_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads Configuration
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    ALLOWED_EXTENSIONS = {"pdf", "wav", "webm", "mp4", "mp3"}
    # Max file size: 30MB
    MAX_CONTENT_LENGTH = 30 * 1024 * 1024

    # AI Service Keys
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
    
    # Whisper settings
    WHISPER_MODEL_NAME = os.environ.get("WHISPER_MODEL_NAME", "tiny")
