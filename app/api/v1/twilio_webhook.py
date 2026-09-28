from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.session import get_db
from app.services.twilio_service import send_twilio_message
from app.services.ai_service import get_agricultural_advice
from app.services import farmer_service
from app.services.weather_service import detect_location, get_weather, format_weather_context
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


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
        # Twilio sends numbers as "whatsapp:+50512345678"
        phone = From.replace("whatsapp:", "")
        user_text = Body.strip()

        if not phone or not user_text:
            return {"status": "ignored"}

        logger.info(f"Twilio message received from {phone}: {user_text[:60]}")

        # Register farmer if not yet in DB
        farmer_service.get_or_create_farmer(db, phone)

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

        # Send reply via Twilio
        await send_twilio_message(to=phone, body=reply)

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Twilio webhook error: {e}")
        return {"status": "ok"}
