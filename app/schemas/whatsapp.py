from pydantic import BaseModel
from typing import Optional, List


# ── WhatsApp Webhook payload schemas ─────────────────────────────────────────

class WhatsAppProfile(BaseModel):
    name: Optional[str] = None


class WhatsAppContact(BaseModel):
    profile: Optional[WhatsAppProfile] = None
    wa_id: str


class WhatsAppTextBody(BaseModel):
    body: str


class WhatsAppImageBody(BaseModel):
    id: str
    mime_type: Optional[str] = None
    caption: Optional[str] = None


class WhatsAppMessage(BaseModel):
    from_: str
    id: str
    timestamp: str
    type: str
    text: Optional[WhatsAppTextBody] = None
    image: Optional[WhatsAppImageBody] = None

    class Config:
        populate_by_name = True
        fields = {"from_": "from"}


class WhatsAppValue(BaseModel):
    messaging_product: str
    contacts: Optional[List[WhatsAppContact]] = []
    messages: Optional[List[WhatsAppMessage]] = []


class WhatsAppChange(BaseModel):
    value: WhatsAppValue
    field: str


class WhatsAppEntry(BaseModel):
    id: str
    changes: List[WhatsAppChange]


class WhatsAppWebhookPayload(BaseModel):
    object: str
    entry: List[WhatsAppEntry]
