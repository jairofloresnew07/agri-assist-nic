import httpx
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

WHATSAPP_API_URL = (
    f"https://graph.facebook.com/v19.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
)


async def send_text_message(to: str, body: str) -> dict:
    """Send a plain text WhatsApp message to a phone number."""
    if not settings.WHATSAPP_ACCESS_TOKEN:
        logger.warning(f"WHATSAPP_ACCESS_TOKEN not configured. Skipping send to {to}.")
        logger.info(f"[DEV] Message that would be sent to {to}: {body}")
        return {}

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": body},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(WHATSAPP_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        logger.info(f"Message sent to {to}")
        return response.json()
