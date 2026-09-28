from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # App
    APP_NAME: str = "AgriAssist NIC"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # WhatsApp / Meta Cloud API
    WHATSAPP_VERIFY_TOKEN: str = ""
    WHATSAPP_ACCESS_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""

    # Twilio WhatsApp Sandbox
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_SANDBOX_NUMBER: str = "+14155238886"

    # AI (Google Gemini)
    GEMINI_API_KEY: str = ""

    # Database
    DATABASE_URL: str = "postgresql://agriuser:agripass@localhost:5432/agriassist"

    # Weather API
    OPENWEATHER_API_KEY: str = ""
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"

    def get_database_url(self) -> str:
        """Return DATABASE_URL with correct scheme for SQLAlchemy 2.x."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        return url


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
