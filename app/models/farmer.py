from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlalchemy.sql import func
from app.db.base import Base


class Farmer(Base):
    """Represents a farmer registered in the system."""
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=True)
    location = Column(String(200), nullable=True)      # e.g. "Matagalpa, Nicaragua"
    main_crops = Column(String(500), nullable=True)    # e.g. "maíz, frijol, café"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class MessageLog(Base):
    """Logs every conversation message for context and analytics."""
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    direction = Column(String(10), nullable=False)     # "inbound" | "outbound"
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text") # "text" | "image" | "audio"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
