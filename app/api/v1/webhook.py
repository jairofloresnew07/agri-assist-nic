from fastapi import APIRouter, Request, HTTPException, Query, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from app.config import settings
from app.db.session import get_db
from app.schemas.whatsapp import WhatsAppWebhookPayload
from app.services.whatsapp_service import send_text_message
from app.services.ai_service import get_agricultural_advice
from app.services import farmer_service
from app.services.weather_service import detect_location, get_weather, format_weather_context
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """WhatsApp webhook verification endpoint required by Meta."""
    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook verified successfully.")
        return PlainTextResponse(content=hub_challenge)
    raise HTTPException(status_code=403, detail="Verification token mismatch.")


@router.post("/webhook")
async def receive_message(request: Request, db: Session = Depends(get_db)):
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

                    # Register farmer if not yet in DB
                    farmer_service.get_or_create_farmer(db, phone)

                    if msg_type == "text" and message.text:
                        user_text = message.text.body
                        logger.info(f"Message received from {phone}: {user_text[:60]}")

                        # Persist inbound message
                        farmer_service.log_message(db, phone, "inbound", user_text)

                        # Get recent history for context
                        history = farmer_service.get_recent_history(db, phone)

                        # Detect location and fetch real-time weather if found
                        weather_context = None
                        city = detect_location(user_text)
                        if city:
                            weather = await get_weather(city)
                            if weather:
                                weather_context = format_weather_context(weather)
                                logger.info(f"Weather context added for {city}")

                        # Generate AI response
                        reply = await get_agricultural_advice(
                            user_text, phone, history, weather_context
                        )

                        # Persist outbound message
                        farmer_service.log_message(db, phone, "outbound", reply)

                        await send_text_message(to=phone, body=reply)

                    elif msg_type == "image":
                        response_text = (
                            "Imagen recibida. El analisis visual de cultivos estara "
                            "disponible proximamente. Por ahora, describe lo que observas "
                            "en tu planta y te orientamos."
                        )
                        farmer_service.log_message(db, phone, "outbound", response_text, "image")
                        await send_text_message(to=phone, body=response_text)

                    else:
                        response_text = "Hola, soy AgriBot. Escribe tu consulta agricola y te ayudo."
                        farmer_service.log_message(db, phone, "outbound", response_text)
                        await send_text_message(to=phone, body=response_text)

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return {"status": "ok"}
