import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_admin_health_returns_healthy_with_db():
    mock_db = MagicMock()
    mock_db.execute.return_value = None

    with patch("app.db.session.get_db", return_value=iter([mock_db])):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/admin/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


@pytest.mark.asyncio
async def test_admin_stats_requires_api_key():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/admin/stats")
    assert response.status_code in (403, 503)


@pytest.mark.asyncio
async def test_admin_stats_rejects_wrong_key():
    with patch("app.api.v1.admin.settings") as mock_settings:
        mock_settings.ADMIN_API_KEY = "correct_key"
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(
                "/api/v1/admin/stats",
                headers={"X-Admin-API-Key": "wrong_key"},
            )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_stats_returns_counts_with_valid_key():
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_query.scalar.return_value = 5
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query

    with patch("app.api.v1.admin.settings") as mock_settings, \
         patch("app.db.session.get_db", return_value=iter([mock_db])):
        mock_settings.ADMIN_API_KEY = "test_admin_key"
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(
                "/api/v1/admin/stats",
                headers={"X-Admin-API-Key": "test_admin_key"},
            )

    assert response.status_code == 200
    data = response.json()
    assert "farmers" in data
    assert "messages" in data


@pytest.mark.asyncio
async def test_twilio_webhook_rejects_oversized_message():
    mock_db = MagicMock()
    long_message = "a" * 2001

    with patch("app.db.session.get_db", return_value=iter([mock_db])):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/v1/twilio/webhook",
                data={"From": "whatsapp:+50512345678", "Body": long_message, "NumMedia": "0"},
            )

    assert response.status_code == 200
    assert "demasiado largo" in response.text
