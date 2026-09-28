from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.v1 import webhook, twilio_webhook, admin

setup_logging(debug=settings.DEBUG)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    setup_logging(debug=settings.DEBUG)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered agricultural assistant for Nicaraguan farmers via WhatsApp",
    lifespan=lifespan,
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(webhook.router, prefix="/api/v1", tags=["WhatsApp Webhook"])
app.include_router(twilio_webhook.router, prefix="/api/v1/twilio", tags=["Twilio Webhook"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])


@app.get("/", tags=["Health"])
async def root():
    return {"app": settings.APP_NAME, "version": settings.APP_VERSION, "status": "running"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
