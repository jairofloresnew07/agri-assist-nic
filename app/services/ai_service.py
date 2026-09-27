import google.generativeai as genai
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)

SYSTEM_PROMPT = """
Eres AgriBot, un asistente agrícola especializado en cultivos de Nicaragua.
Tu misión es ayudar a pequeños agricultores nicaragüenses con:
- Identificación de plagas y enfermedades en sus cultivos
- Recomendaciones de siembra según la época del año
- Consejos de fertilización y riego
- Información sobre el clima y su impacto en los cultivos
- Precios de referencia del mercado local

Cultivos principales que conoces: maíz, frijol, café, caña de azúcar,
arroz, yuca, chiltoma, tomate, plátano/banano, cacao, sorgo.

Responde siempre en español simple y claro, como si hablaras con un
agricultor. Usa términos locales nicaragüenses cuando sea posible.
Sé breve y práctico — máximo 3 párrafos cortos por respuesta.
Si el agricultor manda una foto, analiza visualmente el cultivo.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT,
)


async def get_agricultural_advice(user_message: str, phone_number: str) -> str:
    """Get AI-powered agricultural advice for a farmer's query."""
    try:
        logger.info(f"Generating advice for {phone_number}: {user_message[:50]}...")
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        logger.error(f"AI service error: {e}")
        return (
            "Lo siento, en este momento no puedo procesar tu consulta. "
            "Por favor inténtalo de nuevo en unos minutos. 🌱"
        )
