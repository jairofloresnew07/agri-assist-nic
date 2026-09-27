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


async def get_agricultural_advice(user_message: str, phone_number: str) -> str:
    """Generate agricultural advice for a given farmer query using Gemini."""
    try:
        logger.info(f"Generating advice for {phone_number}: {user_message[:50]}...")
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        logger.error(f"AI service error for {phone_number}: {e}")
        return (
            "En este momento no es posible procesar tu consulta. "
            "Por favor intentalo de nuevo en unos minutos."
        )
