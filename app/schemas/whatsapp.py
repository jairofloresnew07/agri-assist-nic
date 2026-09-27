from pydantic import BaseModel, Field
from pydantic import ConfigDict
from typing import Optional, List


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
    model_config = ConfigDict(populate_by_name=True)

    from_: str = Field(alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[WhatsAppTextBody] = None
    image: Optional[WhatsAppImageBody] = None


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
