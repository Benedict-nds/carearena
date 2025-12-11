# CareArena Backend

Backend API for CareArena - a healthcare education platform providing voice, WhatsApp, and SMS-based patient education.

## Project Structure

```
carearena-backend/
├── app/
│   ├── api/                     # All API routers grouped by domain
│   │   ├── v1/
│   │   │   ├── patients.py
│   │   │   ├── hospitals.py
│   │   │   ├── content.py       # Lessons, conditions, versions
│   │   │   ├── sessions.py      # Conversation sessions API
│   │   │   ├── schedule.py
│   │   │   ├── audit.py
│   │   │   ├── auth.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── core/                    # Core app settings & utilities
│   │   ├── config.py            # ENV, secrets, settings
│   │   ├── security.py          # Auth tokens, roles
│   │   ├── logging_config.py
│   │   └── __init__.py
│   │
│   ├── db/
│   │   ├── database.py          # SQLAlchemy engine, session maker
│   │   ├── base.py              # BaseModel
│   │   ├── models/              # ORM models
│   │   │   ├── patient.py
│   │   │   ├── hospital.py
│   │   │   ├── content.py
│   │   │   ├── conversation.py
│   │   │   ├── scheduling.py
│   │   │   ├── audit.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── patient.py
│   │   ├── hospital.py
│   │   ├── content.py
│   │   ├── session.py
│   │   ├── schedule.py
│   │   ├── audit.py
│   │   └── __init__.py
│   │
│   ├── services/                # Business logic, not tied to HTTP
│   │   ├── patient_service.py
│   │   ├── content_service.py
│   │   ├── session_service.py
│   │   ├── call_service.py      # Outbound call logic
│   │   ├── scheduler_service.py # Scheduling logic
│   │   ├── ai_service.py        # LLM/ASR/TTS calls
│   │   ├── csv_importer.py      # Hospital CSV sync logic
│   │   ├── safety_service.py    # Medical safety guardrails
│   │   ├── escalation_service.py
│   │   └── __init__.py
│   │
│   ├── workflows/               # State machines & orchestrations
│   │   ├── conversation_fsm.py  # ALL states for voice agent
│   │   ├── call_flow.py         # Orchestrator for IVR conversation
│   │   ├── whatsapp_flow.py
│   │   ├── sms_flow.py
│   │   ├── emergency_flow.py
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   ├── phone_utils.py
│   │   ├── time_utils.py
│   │   ├── language_utils.py
│   │   ├── audio_utils.py
│   │   └── __init__.py
│   │
│   ├── main.py                  # FastAPI entry point
│   └── __init__.py
│
├── migrations/                  # Alembic migration scripts
│   ├── env.py
│   ├── versions/
│   └── README
│
├── scripts/                     # Management scripts
│   ├── run_scheduler.py
│   ├── import_csv_manual.py
│   └── seed_content.py
│
├── tests/                       # Unit + integration tests
│   ├── test_patients.py
│   ├── test_content.py
│   ├── test_sessions.py
│   ├── test_scheduler.py
│   └── __init__.py
│
├── .env                         # Environment variables
├── requirements.txt             # Python deps
├── README.md
└── alembic.ini
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

4. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Development

- Run tests: `pytest`
- Create migration: `alembic revision --autogenerate -m "description"`
- Apply migrations: `alembic upgrade head`

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

# carearena
