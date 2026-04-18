"""
API Configuration
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_WORKERS = int(os.getenv("API_WORKERS", 1))

# CORS Settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Session Settings
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", 3600))  # 1 hour
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 50 * 1024 * 1024))  # 50MB

# Vector Store Settings
VECTOR_STORE_DIR = BASE_DIR / "chroma_db"
VECTOR_STORE_DIR.mkdir(exist_ok=True)

# Temp Files
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
