# Multi-Agent AI Chatbot for Document & PPT Generation

A modern multi-agent AI workspace for uploading documents, PDFs, PPT/PPTX files, and images, then using AI to analyze content, retrieve enterprise knowledge, research web context, and generate or revise editable business artifacts.

This project is designed as a full-stack prototype for enterprise content workflows, combining:

- AI-powered document and presentation analysis
- LangGraph-based multi-agent orchestration
- RAG-style enterprise knowledge retrieval
- web research integration
- editable DOCX/PPTX generation
- conversational revision and versioning
- traceability and validation metadata

## Features

- Upload and track document, presentation, and image files
- Create chat conversations for each project or use case
- Analyze uploaded content and extract core structure
- Route requests through a multi-agent workflow
- Retrieve internal enterprise knowledge with RAG
- Research external information through a research service
- Generate DOCX and PPTX outputs from AI-driven templates
- Apply iterative edits with artifact versioning
- Validate generated content and keep traceability metadata
- Support local demo mode and provider-aware live LLM configuration

## Tech stack

- Backend: FastAPI, SQLAlchemy, JWT auth
- Frontend: React + Vite + Tailwind CSS
- Agent orchestration: LangGraph
- Document & presentation generation: python-docx, python-pptx
- OCR and document processing: PyMuPDF, pytesseract, OpenCV, Pillow
- Retrieval: vector search with mock fallback and Pinecone-ready abstraction
- LLM integration: OpenAI-compatible providers with safe fallback behavior
- Containerization: Docker Compose

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
│   ├── requirements.txt
│   └── .venv/
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── index.html
├── tests/
├── .env.example
├── .gitignore
├── .dockerignore
├── docker-compose.yml
├── README.md
├── storage/
└── app.db
```

## Architecture overview

The system follows a modular layered design:

1. Frontend chat + upload experience
2. FastAPI API layer with auth and conversation state
3. Multi-agent orchestration with LangGraph
4. Analysis, research, and retrieval services
5. Generation and editing pipelines for DOCX/PPTX outputs
6. Validation and traceability layer for quality checks

## Local setup

### 1) Create Python environment

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Configure environment

From the repo root:

```powershell
Copy-Item .env.example .env
```

### 3) Run backend

```powershell
cd backend
$env:PYTHONPATH = "backend"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4) Run frontend

```powershell
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Open the app at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Docker

From the root folder:

```powershell
docker compose up --build
```

This starts:

- backend on port 8000
- frontend on port 3000

## Demo login

The project supports a built-in local demo account:

- Email: demo@example.com
- Password: demo1234

## Testing

Run verification from the repository root:

```powershell
$env:PYTHONPATH = "backend"
python -m pytest -q --disable-plugin-autoload
```

## Core API endpoints

- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/conversations
- POST /api/v1/conversations
- POST /api/v1/chat
- POST /api/v1/upload
- POST /api/v1/analyze
- POST /api/v1/orchestrate

## Notes

- The app supports a local demo/mock mode for quick development and validation.
- Real provider integration is possible by adding environment keys and switching to live service configuration.
- Artifact generation and revision flows are organized to support future enterprise-grade production workflows.

## GitHub readiness

This repository is prepared for public/follow-along usage with:

- environment-based settings
- modular backend/frontend architecture
- Docker-based local execution
- a staged validation suite covering orchestration, generation, editing, research, and LLM integration
- no secrets or credentials committed by default

## License

This project is intended for educational and prototype/demo use.
