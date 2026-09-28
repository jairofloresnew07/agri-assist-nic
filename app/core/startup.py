from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def validate_required_settings() -> None:
    """
    Validate that all required environment variables are configured.
    Raises RuntimeError at startup if any critical setting is missing.
    """
    errors = []

    if not settings.GEMINI_API_KEY:
        errors.append("GEMINI_API_KEY is not set.")

    if not settings.DATABASE_URL:
        errors.append("DATABASE_URL is not set.")

    if not settings.WHATSAPP_VERIFY_TOKEN:
        errors.append("WHATSAPP_VERIFY_TOKEN is not set.")

    if not settings.ADMIN_API_KEY:
        logger.warning("ADMIN_API_KEY is not set. Admin endpoints will be unavailable.")

    if errors:
        for error in errors:
            logger.error(f"Configuration error: {error}")
        raise RuntimeError(
            f"Server cannot start due to missing configuration: {'; '.join(errors)}"
        )

    logger.info("Configuration validated successfully.")
