import google.generativeai as genai
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)

SYSTEM_PROMPT = """
Eres AgriBot, un asistente agricola especializado en cultivos de Nicaragua.
Tu mision es ayudar a pequeños agricultores nicaraguenses con:
- Identificacion de plagas y enfermedades en sus cultivos
- Recomendaciones de siembra segun la epoca del año
- Consejos de fertilizacion y riego
- Informacion sobre el clima y su impacto en los cultivos
- Precios de referencia del mercado local

Cultivos principales: maiz, frijol, cafe, cana de azucar, arroz, yuca,
chiltoma, tomate, platano, banano, cacao, sorgo.

Responde siempre en español claro y directo. Usa terminos locales
nicaraguenses cuando corresponda. Maximo 3 parrafos cortos por respuesta.
Si el agricultor envia una imagen, analiza visualmente el cultivo.
"""

model = genai.GenerativeModel(
    model_name="gemini-3.8-flash",
    system_instruction=SYSTEM_PROMPT,
)


def _build_prompt(
    user_message: str,
    history: list,
    weather_context: str | None = None,
) -> str:
    """Build a prompt including conversation history and weather context."""
    parts = []

    if weather_context:
        parts.append(f"Informacion climatica actual: {weather_context}")

    if history:
        context_lines = []
        for entry in reversed(history):
            role = "Agricultor" if entry.direction == "inbound" else "AgriBot"
            context_lines.append(f"{role}: {entry.content}")
        parts.append("Historial reciente:\n" + "\n".join(context_lines))

    parts.append(f"Nueva consulta: {user_message}")
    return "\n\n".join(parts)


async def get_agricultural_advice(
    user_message: str,
    phone_number: str,
    history: list | None = None,
    weather_context: str | None = None,
) -> str:
    """Generate agricultural advice using Gemini, with optional conversation history and weather data."""
    try:
        prompt = _build_prompt(user_message, history or [], weather_context)
        logger.info(f"Generating advice for {phone_number}: {user_message[:50]}...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"AI service error for {phone_number}: {e}")
        return (
            "En este momento no es posible procesar tu consulta. "
            "Por favor intentalo de nuevo en unos minutos."
        )
