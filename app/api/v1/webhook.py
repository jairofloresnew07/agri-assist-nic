from fastapi import APIRouter, Request, HTTPException, Query
from app.config import settings
from app.schemas.whatsapp import WhatsAppWebhookPayload
from app.services.whatsapp_service import send_text_message
from app.services.ai_service import get_agricultural_advice
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """WhatsApp webhook verification endpoint (Meta handshake)."""
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification token mismatch")


@router.post("/webhook")
async def receive_message(request: Request):
    """Receive and process incoming WhatsApp messages."""
    try:
        body = await request.json()
        payload = WhatsAppWebhookPayload(**body)

        for entry in payload.entry:
            for change in entry.changes:
                if not change.value.messages:
                    continue

                for message in change.value.messages:
                    phone = message.from_
                    msg_type = message.type

                    if msg_type == "text" and message.text:
                        user_text = message.text.body
                        logger.info(f"Received from {phone}: {user_text[:60]}")

                        reply = await get_agricultural_advice(user_text, phone)
                        await send_text_message(to=phone, body=reply)

                    elif msg_type == "image":
                        await send_text_message(
                            to=phone,
                            body=(
                                "📸 Recibí tu foto. Pronto podremos analizar imágenes "
                                "de cultivos. Por ahora, descríbeme qué observas en tu planta."
                            ),
                        )
                    else:
                        await send_text_message(
                            to=phone,
                            body="Hola 👋 Soy AgriBot. Escríbeme tu consulta agrícola y te ayudo.",
                        )

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return {"status": "ok"}  # Always return 200 to WhatsApp
