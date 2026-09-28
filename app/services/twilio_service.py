import httpx
from twilio.rest import Client
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


async def send_twilio_message(to: str, body: str) -> dict:
    """Send a WhatsApp message via Twilio sandbox."""
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        logger.warning("Twilio credentials not configured. Skipping send.")
        logger.info(f"[DEV] Message that would be sent to {to}: {body}")
        return {}

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_=f"whatsapp:{settings.TWILIO_SANDBOX_NUMBER}",
            to=f"whatsapp:{to}",
            body=body,
        )
        logger.info(f"Twilio message sent to {to} — SID: {message.sid}")
        return {"sid": message.sid, "status": message.status}
    except Exception as e:
        logger.error(f"Twilio send error to {to}: {e}")
        return {}
