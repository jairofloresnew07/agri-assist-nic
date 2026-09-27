import httpx
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

BASE_URL = settings.OPENWEATHER_BASE_URL

NICARAGUA_CITIES = {
    "managua": "Managua,NI",
    "leon": "Leon,NI",
    "granada": "Granada,NI",
    "matagalpa": "Matagalpa,NI",
    "esteli": "Esteli,NI",
    "chinandega": "Chinandega,NI",
    "masaya": "Masaya,NI",
    "jinotega": "Jinotega,NI",
    "rivas": "Rivas,NI",
    "boaco": "Boaco,NI",
    "chontales": "Juigalpa,NI",
    "nueva segovia": "Ocotal,NI",
    "madriz": "Somoto,NI",
    "carazo": "Jinotepe,NI",
    "rio san juan": "San Carlos,NI",
    "jalapa": "Jalapa,NI",
    "ocotal": "Ocotal,NI",
    "somoto": "Somoto,NI",
    "jinotepe": "Jinotepe,NI",
    "juigalpa": "Juigalpa,NI",
}


def detect_location(text: str) -> str | None:
    """Detect a Nicaraguan city or department name in a message."""
    text_lower = text.lower()
    for keyword, city_query in NICARAGUA_CITIES.items():
        if keyword in text_lower:
            return city_query
    return None


async def get_weather(city_query: str) -> dict | None:
    """Fetch current weather data from OpenWeatherMap for a given city."""
    if not settings.OPENWEATHER_API_KEY:
        logger.warning("OPENWEATHER_API_KEY not configured. Skipping weather fetch.")
        return None

    params = {
        "q": city_query,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "es",
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{BASE_URL}/weather", params=params)
            response.raise_for_status()
            data = response.json()

            weather = {
                "ciudad": data["name"],
                "temperatura": round(data["main"]["temp"], 1),
                "humedad": data["main"]["humidity"],
                "descripcion": data["weather"][0]["description"],
                "viento_kmh": round(data["wind"]["speed"] * 3.6, 1),
                "lluvia_mm": data.get("rain", {}).get("1h", 0),
            }
            logger.info(f"Weather fetched for {city_query}: {weather['temperatura']}C, {weather['descripcion']}")
            return weather

    except httpx.HTTPStatusError as e:
        logger.warning(f"Weather API HTTP error for {city_query}: {e.response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Weather API error for {city_query}: {e}")
        return None


def format_weather_context(weather: dict) -> str:
    """Format weather data as a readable string for the AI prompt."""
    return (
        f"Clima actual en {weather['ciudad']}: "
        f"{weather['temperatura']}°C, {weather['descripcion']}, "
        f"humedad {weather['humedad']}%, "
        f"viento {weather['viento_kmh']} km/h, "
        f"lluvia ultima hora {weather['lluvia_mm']} mm."
    )
