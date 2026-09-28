from fastapi import APIRouter, Request, Depends, Form, Response
from sqlalchemy.orm import Session
from typing import Annotated
from xml.sax.saxutils import escape as xml_escape
from app.db.session import get_db
from app.services.ai_service import get_agricultural_advice
from app.services import farmer_service
from app.services.weather_service import detect_location, get_weather, format_weather_context
from app.core.rate_limiter import is_rate_limited, seconds_until_reset
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


def _twiml(message: str) -> Response:
    """Build a TwiML XML response with a single message, safely escaped."""
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{xml_escape(message)}</Message>
</Response>"""
    return Response(content=xml, media_type="application/xml")


@router.post("/webhook")
async def twilio_receive_message(
    request: Request,
    db: Session = Depends(get_db),
    From: Annotated[str, Form()] = "",
    Body: Annotated[str, Form()] = "",
    NumMedia: Annotated[str, Form()] = "0",
):
    """Receive and process incoming WhatsApp messages from Twilio sandbox."""
    try:
        phone = From.replace("whatsapp:", "")
        user_text = Body.strip()

        if not phone or not user_text:
            return Response(content="<?xml version='1.0'?><Response/>", media_type="application/xml")

        logger.info(f"Twilio message received from {phone}: {user_text[:60]}")

        # Register farmer if not yet in DB
        farmer_service.get_or_create_farmer(db, phone)

        # Enforce rate limit before calling AI
        if is_rate_limited(phone):
            wait = seconds_until_reset(phone)
            return _twiml(
                f"Has enviado muchos mensajes seguidos. "
                f"Por favor espera {wait} segundos antes de consultar de nuevo."
            )

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
        reply = await get_agricultural_advice(user_text, phone, history, weather_context)

        # Persist outbound message
        farmer_service.log_message(db, phone, "outbound", reply)

        return _twiml(reply)

    except Exception as e:
        logger.error(f"Twilio webhook error: {e}")
        return Response(
            content="<?xml version='1.0' encoding='UTF-8'?><Response/>",
            media_type="application/xml",
        )
