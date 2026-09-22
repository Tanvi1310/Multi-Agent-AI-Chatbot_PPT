# Multi-Agent AI Chatbot for Document & PPT Generation

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react" alt="React" />
  <img src="https://img.shields.io/badge/LangGraph-MultiAgent-8A2BE2?style=for-the-badge" alt="LangGraph" />
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" alt="Docker" />
</p>

<p align="center">
  <strong>AI-powered document, presentation, and enterprise knowledge workflow builder.</strong>
</p>

A full-stack prototype for uploading documents, PDFs, PPT/PPTX files, and images, then using a multi-agent AI system to analyze content, retrieve enterprise knowledge, research web context, and generate or revise editable business artifacts.

## Why this project

This project helps teams automate the messy middle layer between raw knowledge and polished business output:

- upload source documents and presentations
- understand the content structure and intent
- enrich the request with internal knowledge and external research
- generate or revise DOCX/PPTX deliverables
- keep traceability, validation, and version continuity

It is built as a practical enterprise POC that demonstrates how AI agents can collaborate around a real document workflow.

## Core features

- Upload and manage DOCX, PDF, PPT/PPTX, and image files
- Create conversations and track artifacts by session
- Analyze uploaded files to extract headings, text, and slide structure
- Orchestrate requests through a LangGraph multi-agent workflow
- Pull retrieval context from an internal enterprise knowledge base
- Perform research-aware content enhancement
- Generate editable DOCX and PPTX outputs
- Support conversational edits and revision history
- Validate generated output and attach traceability metadata
- Run in local demo mode with safe provider fallback

## Tech stack

- Backend: FastAPI, SQLAlchemy, JWT auth
- Frontend: React + Vite + Tailwind CSS
- Orchestration: LangGraph
- Document generation: python-docx, python-pptx
- OCR / document parsing: PyMuPDF, pytesseract, OpenCV, Pillow
- Retrieval: vector-search abstraction with mock + Pinecone-ready support
- LLM access: OpenAI-compatible providers with safe fallback
- Deployment: Docker Compose

## Architecture overview

```text
Frontend UI
   ↓
FastAPI API
   ↓
Auth + Conversation + Artifact storage
   ↓
Supervisor + LangGraph agents
   ├── document analysis
   ├── PPT analysis
   ├── OCR / image handling
   ├── web research
   ├── enterprise RAG
   ├── generation
   ├── validation
   └── editing/versioning
```

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
├── app.db
└── .env
```

## Quick start

### 1) Set up Python environment

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Create environment file

From the repository root:

```powershell
Copy-Item .env.example .env
```

### 3) Start the backend

```powershell
cd backend
$env:PYTHONPATH = "backend"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4) Start the frontend

```powershell
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

### 5) Open the app

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Docker setup

```powershell
docker compose up --build
```

## Demo credentials

The app ships with a local demo login for quick testing:

- Email: demo@example.com
- Password: demo1234

## Testing

Run the test suite from the project root:

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

## Use cases

This prototype is suitable for:

- sales proposal generation
- internal research synthesis
- executive deck summarization
- content adaptation from uploaded templates
- document-to-presentation workflows
- enterprise knowledge assistants

## Notes

- Local demo mode is intentionally included for easy setup and validation.
- Real providers can be configured through environment variables when live AI access is required.
- The generation and versioning layer is designed to support iterative enterprise content workflows.

## License

This project is intended for educational, prototype, and demonstrator use.
