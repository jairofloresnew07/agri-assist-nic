import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock
from app.main import app
from app.config import settings


@pytest.mark.asyncio
async def test_webhook_verification_valid_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/webhook", params={
            "hub.mode": "subscribe",
            "hub.verify_token": settings.WHATSAPP_VERIFY_TOKEN,
            "hub.challenge": "abc123",
        })
    assert response.status_code == 200
    assert response.text == "abc123"


@pytest.mark.asyncio
async def test_webhook_verification_invalid_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/webhook", params={
            "hub.mode": "subscribe",
            "hub.verify_token": "token_equivocado",
            "hub.challenge": "abc123",
        })
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_twilio_webhook_ignores_empty_body():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/twilio/webhook",
            data={"From": "", "Body": "", "NumMedia": "0"},
        )
    assert response.status_code == 200
    assert "Response" in response.text


@pytest.mark.asyncio
async def test_twilio_webhook_returns_twiml_on_message():
    """Verify the webhook returns valid TwiML when a message is received."""
    mock_db = MagicMock()

    with patch("app.api.v1.twilio_webhook.farmer_service.get_or_create_farmer"), \
         patch("app.api.v1.twilio_webhook.farmer_service.log_message"), \
         patch("app.api.v1.twilio_webhook.farmer_service.get_recent_history", return_value=[]), \
         patch("app.api.v1.twilio_webhook.get_agricultural_advice", return_value="Respuesta de prueba"), \
         patch("app.api.v1.twilio_webhook.detect_location", return_value=None), \
         patch("app.db.session.get_db", return_value=iter([mock_db])):

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v1/twilio/webhook",
                data={
                    "From": "whatsapp:+50512345678",
                    "Body": "Mis plantas tienen manchas",
                    "NumMedia": "0",
                },
            )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/xml")
    assert "<Response>" in response.text
    assert "<Message>" in response.text


@pytest.mark.asyncio
async def test_twilio_webhook_rate_limit_response():
    """Verify rate-limited requests receive a polite TwiML message."""
    phone = "whatsapp:+50599999001"
    mock_db = MagicMock()

    with patch("app.api.v1.twilio_webhook.farmer_service.get_or_create_farmer"), \
         patch("app.api.v1.twilio_webhook.is_rate_limited", return_value=True), \
         patch("app.api.v1.twilio_webhook.seconds_until_reset", return_value=30), \
         patch("app.db.session.get_db", return_value=iter([mock_db])):

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v1/twilio/webhook",
                data={"From": phone, "Body": "consulta", "NumMedia": "0"},
            )

    assert response.status_code == 200
    assert "espera" in response.text.lower() or "30" in response.text
