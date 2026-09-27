# AgriAssist NIC

**Asistente agrícola basado en IA para pequeños agricultores nicaragüenses, accesible vía WhatsApp.**

[![CI](https://github.com/jairofloresnew07/agri-assist-nic/actions/workflows/ci.yml/badge.svg)](https://github.com/jairofloresnew07/agri-assist-nic/actions)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Problema

Miles de agricultores nicaragüenses pierden cosechas cada año por falta de acceso oportuno a información agrícola: identificación de plagas, recomendaciones de riego, pronósticos climáticos y precios de mercado. Un agrónomo presencial es costoso e inaccesible para comunidades rurales.

## Solución

AgriAssist NIC es un chatbot inteligente accesible vía WhatsApp, la aplicación más utilizada en Nicaragua incluso con conexión básica a internet. Los agricultores pueden consultar sobre diagnóstico de plagas, recomendaciones de siembra, fertilización, clima y precios de mercado local.

## Arquitectura

```
Agricultor (WhatsApp)
        |
        v
  Meta WhatsApp API
        |
        v
  FastAPI Backend  <---> Google Gemini AI
        |
        v
   PostgreSQL DB
```

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Backend | FastAPI (Python 3.13) |
| IA | Google Gemini 1.5 Flash |
| Base de datos | PostgreSQL 16 |
| Mensajería | WhatsApp Cloud API (Meta) |
| Infraestructura | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Deploy | Railway / Render |

## Configuración local

### Prerequisitos

- Python 3.13+
- Docker Desktop
- Git

### Instalación

```bash
git clone https://github.com/jairofloresnew07/agri-assist-nic.git
cd agri-assist-nic

py -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

### Variables de entorno

```bash
copy .env.example .env
# Completar .env con las API keys correspondientes
```

### Ejecución

```bash
# Levantar base de datos
docker-compose up db -d

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Documentación: http://localhost:8000/docs

### Tests

```bash
pytest tests/ -v
```

## Estructura del proyecto

```
agri-assist-nic/
├── app/
│   ├── api/v1/          # Endpoints de la API
│   ├── core/            # Logging y utilidades base
│   ├── db/              # Sesión y declaraciones SQLAlchemy
│   ├── models/          # Modelos de base de datos
│   ├── schemas/         # Schemas Pydantic para validación
│   ├── services/        # Lógica de negocio (IA, WhatsApp)
│   ├── config.py        # Configuración centralizada
│   └── main.py          # Entrada de la aplicación
├── tests/
├── .github/workflows/
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Autor

Jairo Flores — [@jairofloresnew07](https://github.com/jairofloresnew07)

## Licencia

MIT — ver [LICENSE](LICENSE)
