# AgriAssist NIC

Asistente agrícola conversacional para Nicaragua, entregado via WhatsApp. Combina inteligencia artificial generativa con datos climaticos en tiempo real para proporcionar orientacion tecnica contextualizada a agricultores nicaraguenses.

---

## Descripcion

AgriAssist NIC recibe mensajes de WhatsApp de agricultores, los procesa mediante Google Gemini con contexto de conversacion historica y condiciones climaticas actuales, y devuelve consejo tecnico adaptado a la realidad agricola de Nicaragua.

El sistema distingue cultivos, plagas y condiciones de cada region del pais. Mantiene memoria por agricultor y detecta automaticamente menciones de ubicacion para enriquecer las respuestas con datos meteorologicos vigentes.

---

## Arquitectura

```
WhatsApp (agricultor)
        |
   Twilio Sandbox          (produccion: Meta Cloud API)
        |
   Railway (HTTPS)
        |
   FastAPI — app/main.py
        |
   app/api/v1/twilio_webhook.py
        |
   +-----------------------+
   |                       |
farmer_service         rate_limiter
   |                       |
   DB (PostgreSQL)    weather_service
                           |
                      OpenWeatherMap API
                           |
                      ai_service
                           |
                      Google Gemini
```

---

## Tecnologias

| Componente | Tecnologia |
|---|---|
| Backend | Python 3.13 / FastAPI |
| Base de datos | PostgreSQL + SQLAlchemy + Alembic |
| IA generativa | Google Gemini (gemini-2.5-flash) |
| Clima | OpenWeatherMap API |
| Mensajeria | Twilio WhatsApp Sandbox / Meta Cloud API |
| Produccion | Railway (deploy automatico desde GitHub) |

---

## Estructura del proyecto

```
agri-assist-nic/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── webhook.py          # Meta Cloud API webhook
│   │       └── twilio_webhook.py   # Twilio WhatsApp sandbox webhook
│   ├── core/
│   │   ├── logging.py              # Configuracion de logging
│   │   └── rate_limiter.py        # Control de tasa por numero de telefono
│   ├── db/
│   │   ├── base.py                 # Base declarativa SQLAlchemy
│   │   └── session.py              # Factory de sesiones y dependencia get_db
│   ├── models/
│   │   └── farmer.py               # Modelos Farmer y MessageLog
│   ├── schemas/
│   │   └── whatsapp.py             # Esquemas Pydantic para payload de Meta
│   ├── services/
│   │   ├── ai_service.py           # Integracion con Google Gemini
│   │   ├── farmer_service.py       # CRUD de agricultores e historial
│   │   ├── twilio_service.py       # Envio via Twilio API (modo API)
│   │   ├── weather_service.py      # Deteccion de ubicacion y clima
│   │   └── whatsapp_service.py     # Envio via Meta Cloud API
│   ├── config.py                   # Configuracion centralizada con pydantic-settings
│   └── main.py                     # Punto de entrada FastAPI
├── alembic/                        # Migraciones de base de datos
├── tests/                          # Suite de pruebas
├── Dockerfile
├── docker-compose.yml              # PostgreSQL local para desarrollo
├── requirements.txt
├── start.sh                        # Script de inicio: migraciones + uvicorn
└── .env.example
```

---

## Configuracion del entorno

### Prerequisitos

- Python 3.11+
- Docker (para PostgreSQL local)
- Cuenta en Google AI Studio (Gemini API)
- Cuenta en OpenWeatherMap
- Cuenta en Twilio (sandbox) o Meta for Developers (produccion)

### Instalacion local

```bash
git clone https://github.com/jairofloresnew07/agri-assist-nic.git
cd agri-assist-nic

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

### Variables de entorno

Copia `.env.example` a `.env` y completa los valores:

```bash
cp .env.example .env
```

```env
# Base de datos
DATABASE_URL=postgresql://agriuser:agripass@localhost:5432/agriassist

# Google Gemini
GEMINI_API_KEY=

# OpenWeatherMap
OPENWEATHER_API_KEY=

# Twilio WhatsApp Sandbox
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_SANDBOX_NUMBER=+14155238886

# Meta Cloud API (produccion)
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_VERIFY_TOKEN=

# Aplicacion
DEBUG=true
```

### Base de datos local

```bash
docker compose up -d
alembic upgrade head
```

### Servidor de desarrollo

```bash
uvicorn app.main:app --reload
```

La API queda disponible en `http://localhost:8000`. Documentacion interactiva en `http://localhost:8000/docs`.

---

## Endpoints principales

| Metodo | Endpoint | Descripcion |
|---|---|---|
| GET | `/health` | Estado del servicio |
| GET | `/api/v1/webhook` | Verificacion de webhook Meta |
| POST | `/api/v1/webhook` | Recepcion de mensajes Meta Cloud API |
| POST | `/api/v1/twilio/webhook` | Recepcion de mensajes Twilio sandbox |

---

## Despliegue en produccion

El proyecto se despliega automaticamente en Railway al hacer push a la rama `main`.

El script `start.sh` ejecuta las migraciones de Alembic antes de iniciar el servidor, garantizando que el esquema de base de datos siempre este actualizado.

URL de produccion: `https://agri-assist-nic-production.up.railway.app`

---

## Pruebas

```bash
pytest tests/ -v
```

---

## Limitaciones actuales

- **Twilio Sandbox**: requiere que cada numero de telefono envie `join <codigo>` al `+1 415 523 8886` para activar la sesion. La sesion expira cada 24 horas.
- **Meta Cloud API**: pendiente de aprobacion de dispositivo en Meta for Developers.
- **Rate limiting**: 3 mensajes por minuto por numero de telefono (ventana deslizante en memoria).
- **OpenWeatherMap**: la activacion de una clave nueva puede tardar hasta 2 horas.

---

## Licencia

MIT
