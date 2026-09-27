from sqlalchemy.orm import Session
from app.models.farmer import Farmer, MessageLog
from app.core.logging import get_logger

logger = get_logger(__name__)


def get_or_create_farmer(db: Session, phone_number: str) -> Farmer:
    """Return the existing farmer record or create a new one."""
    farmer = db.query(Farmer).filter(Farmer.phone_number == phone_number).first()
    if not farmer:
        farmer = Farmer(phone_number=phone_number)
        db.add(farmer)
        db.commit()
        db.refresh(farmer)
        logger.info(f"New farmer registered: {phone_number}")
    return farmer


def log_message(
    db: Session,
    phone_number: str,
    direction: str,
    content: str,
    message_type: str = "text",
) -> MessageLog:
    """Persist an inbound or outbound message to the log."""
    entry = MessageLog(
        phone_number=phone_number,
        direction=direction,
        content=content,
        message_type=message_type,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_recent_history(db: Session, phone_number: str, limit: int = 6) -> list[MessageLog]:
    """Return the most recent messages for a given phone number."""
    return (
        db.query(MessageLog)
        .filter(MessageLog.phone_number == phone_number)
        .order_by(MessageLog.created_at.desc())
        .limit(limit)
        .all()
    )
