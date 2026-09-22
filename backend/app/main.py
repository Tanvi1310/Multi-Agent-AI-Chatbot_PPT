from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import Base, engine
from app.models import chat  # noqa: F401  # ensures ORM tables are registered before create_all
from app.api.v1.analysis_routes import analysis_router
from app.api.v1.orchestration_routes import orchestration_router
from app.api.v1.routes import api_router

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0", description="Multi-agent AI Chatbot POC backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.artifacts_dir).mkdir(parents=True, exist_ok=True)
    import app.models.chat  # noqa: F401
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Multi-Agent AI Chatbot backend is running."}


app.include_router(api_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")
app.include_router(orchestration_router, prefix="/api/v1")


@app.exception_handler(Exception)
async def global_exception_handler(_request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": f"Unexpected server error: {exc}"})
