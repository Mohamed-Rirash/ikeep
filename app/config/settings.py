import os
from functools import lru_cache
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # App
    APP_NAME: str = os.getenv("APP_NAME")
    DEBUG: bool = os.getenv("DEBUG") == "True"

    # FrontEnd Application
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST", "http://localhost:3000")

    # Database Config
    USER: str = os.getenv("PUSER")
    PASSWORD: str = os.getenv("PASSWORD")
    DB: str = os.getenv("DB")
    DATABASE_URI: str = f"postgresql://{quote_plus(
        USER)}:{quote_plus(PASSWORD)}@localhost/{DB}"

    # JWT Secret Key
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: str = os.getenv("ACCESS_TOKEN_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 3))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 11000))

    # App Secret Key
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    # Email Configuration
    EMAIL_USER: str = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM")
    EMAIL_PORT: int = int(os.getenv("EMAIL_PORT"))
    EMAIL_SERVER: str = os.getenv("EMAIL_SERVER")
    EMAIL_STARTTLS: bool = os.getenv("EMAIL_TLS") == "True"
    EMAIL_SSL_TLS: bool = os.getenv("EMAIL_SSL") == "True"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
