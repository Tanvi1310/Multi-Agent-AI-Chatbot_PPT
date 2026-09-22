# Multi-Agent AI Chatbot POC

A modular enterprise-grade multi-agent document and presentation generation system built with FastAPI, React, LangGraph, and editable DOCX/PPTX generation.

## Current status

This project is validated through the following phases:

- Phase 1: backend/frontend foundation and chat shell
- Phase 2: analysis pipeline and uploaded-file handling
- Phase 3: orchestration and routing
- Phase 4: web research and RAG retrieval
- Phase 5: DOCX/PPTX generation
- Phase 6: conversational editing and versioning
- Phase 7: validation and traceability
- Phase 8: provider-aware LLM integration with safe fallback

## Tech stack

- Backend: FastAPI, SQLAlchemy, JWT auth
- Frontend: React + Vite + Tailwind CSS
- Agent orchestration: LangGraph
- Research/RAG: mock and Pinecone-ready vector retrieval
- Document generation: python-docx and python-pptx
- OCR/document handling: PyMuPDF, pytesseract, OpenCV, Pillow
- Config: environment-based settings with local demo defaults

## Project structure

```text
.
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models/
│   │   ├── rag/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── generation/
│   ├── Dockerfile
│   ├── pytest.ini
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── sample_templates/
├── storage/
├── tests/
├── .env.example
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── README.md
└── app.db
```

## Local setup

### 1) Python environment

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment

```bash
cp .env.example .env
```

### 3) Run backend

```bash
cd backend
set PYTHONPATH=backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4) Run frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

The application is available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Docker

From the project root:

```bash
docker compose up --build
```

This starts:

- backend on port 8000
- frontend on port 3000

## Demo credentials

The app supports local demo login flow:

- Email: demo@example.com
- Password: demo1234

## Testing

Run the project checks from the repo root:

```bash
set PYTHONPATH=backend
python -m pytest -q --disable-plugin-autoload
```

## API highlights

- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/conversations
- POST /api/v1/conversations
- POST /api/v1/chat
- POST /api/v1/upload
- POST /api/v1/orchestrate

## Notes

- The project intentionally supports a demo/mock mode for local development.
- Real provider integration is safe when valid API keys are inserted into the environment.
- Artifact generation and edit/version flows are designed to preserve a clean revision history.

## GitHub readiness

This repository is structured for a clean public-facing setup with:

- environment-based configuration
- dependency pinning for core runtime packages
- Docker support for local orchestration
- explicit tests for orchestration, research, generation, editing, validation, and provider fallback
- no secret material committed by default
