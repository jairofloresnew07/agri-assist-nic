from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AgriAssist NIC"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # WhatsApp / Twilio
    WHATSAPP_VERIFY_TOKEN: str = ""
    WHATSAPP_ACCESS_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""

    # AI (Google Gemini)
    GEMINI_API_KEY: str = ""

    # Database
    DATABASE_URL: str = "postgresql://agriuser:agripass@localhost:5432/agriassist"

    # Weather API
    OPENWEATHER_API_KEY: str = ""
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
