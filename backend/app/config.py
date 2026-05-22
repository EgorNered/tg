import os
from pydantic_settings import BaseSettings # Если используешь pydantic v2

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./finance.db")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

settings = Settings()