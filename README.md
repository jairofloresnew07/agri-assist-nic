# 🌱 AgriAssist NIC

> **Asistente agrícola con IA para pequeños agricultores nicaragüenses vía WhatsApp**

[![CI](https://github.com/jairofloresnew07/agri-assist-nic/actions/workflows/ci.yml/badge.svg)](https://github.com/jairofloresnew07/agri-assist-nic/actions)
[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📌 Problema

Miles de agricultores nicaragüenses pierden cosechas cada año por falta de acceso oportuno a información agrícola: identificación de plagas, recomendaciones de riego, pronósticos climáticos y precios de mercado. Un agrónomo presencial es costoso e inaccesible para comunidades rurales.

## 💡 Solución

AgriAssist NIC es un chatbot inteligente accesible vía **WhatsApp** — la app más usada en Nicaragua, incluso con internet básico. Los agricultores pueden:

- 📸 Enviar fotos de sus cultivos para diagnóstico de plagas
- 🌤️ Recibir recomendaciones basadas en el clima de su zona
- 🌱 Consultar sobre siembra, fertilización y cosecha
- 📊 Ver precios de referencia del mercado local

## 🏗️ Arquitectura

```
Agricultor (WhatsApp)
        │
        ▼
  Meta WhatsApp API
        │
        ▼
  FastAPI Backend  ◄──► Google Gemini AI
        │
        ▼
   PostgreSQL DB
```

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Backend | FastAPI (Python 3.13) |
| IA | Google Gemini 1.5 Flash |
| Base de datos | PostgreSQL 16 |
| Mensajería | WhatsApp Cloud API (Meta) |
| Infraestructura | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Deploy | Railway / Render |

## 🚀 Cómo ejecutar localmente

### 1. Prerequisitos
- Python 3.13+
- Docker Desktop
- Git

### 2. Clonar e instalar
```bash
git clone https://github.com/jairofloresnew07/agri-assist-nic.git
cd agri-assist-nic

# Crear entorno virtual
py -m venv venv
venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
copy .env.example .env
# Editar .env con tus API keys reales
```

### 4. Levantar la base de datos
```bash
docker-compose up db -d
```

### 5. Ejecutar la API
```bash
uvicorn app.main:app --reload
```

La API estará disponible en: http://localhost:8000
Documentación interactiva: http://localhost:8000/docs

### 6. Ejecutar tests
```bash
pytest tests/ -v
```

## 📁 Estructura del Proyecto

```
agri-assist-nic/
├── app/
│   ├── api/v1/          # Endpoints (webhook WhatsApp)
│   ├── core/            # Logging y utilidades base
│   ├── db/              # Sesión y base SQLAlchemy
│   ├── models/          # Modelos de base de datos
│   ├── schemas/         # Schemas Pydantic (validación)
│   ├── services/        # Lógica de negocio (AI, WhatsApp)
│   ├── config.py        # Configuración centralizada
│   └── main.py          # Entrada de la aplicación
├── tests/               # Suite de pruebas
├── .github/workflows/   # CI/CD con GitHub Actions
├── docker-compose.yml   # Orquestación de servicios
├── Dockerfile           # Imagen de producción
├── requirements.txt     # Dependencias Python
└── .env.example         # Plantilla de variables de entorno
```

## 👤 Autor

**Jairo Flores** — [@jairofloresnew07](https://github.com/jairofloresnew07)

Estudiante de Ingeniería en Computación | Nicaragua 🇳🇮

## 📄 Licencia

MIT — ver [LICENSE](LICENSE)
