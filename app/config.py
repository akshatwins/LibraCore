import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///library.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOAN_PERIOD_DAYS = int(os.getenv("LOAN_PERIOD_DAYS", "14"))
    FINE_PER_DAY = float(os.getenv("FINE_PER_DAY", "5"))
    ITEMS_PER_PAGE = 10
