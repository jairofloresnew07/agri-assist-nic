from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.db.session import get_db
from app.models.farmer import Farmer, MessageLog
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

_api_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)


def _require_admin_key(api_key: str = Security(_api_key_header)):
    """Validate the admin API key provided in the request header."""
    if not settings.ADMIN_API_KEY:
        raise HTTPException(status_code=503, detail="Admin API key not configured.")
    if api_key != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin API key.")
    return api_key


@router.get("/health", tags=["Admin"])
async def health_with_db(db: Session = Depends(get_db)):
    """
    Deep health check that verifies database connectivity.
    Returns 503 if the database is unreachable.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        raise HTTPException(status_code=503, detail="Database unavailable.")


@router.get("/stats", tags=["Admin"], dependencies=[Depends(_require_admin_key)])
async def get_stats(db: Session = Depends(get_db)):
    """
    System usage statistics. Requires X-Admin-API-Key header.
    """
    total_farmers = db.query(func.count(Farmer.id)).scalar()
    total_messages = db.query(func.count(MessageLog.id)).scalar()
    inbound = db.query(func.count(MessageLog.id)).filter(
        MessageLog.direction == "inbound"
    ).scalar()
    outbound = db.query(func.count(MessageLog.id)).filter(
        MessageLog.direction == "outbound"
    ).scalar()

    return {
        "farmers": {
            "total": total_farmers,
        },
        "messages": {
            "total": total_messages,
            "inbound": inbound,
            "outbound": outbound,
        },
    }
