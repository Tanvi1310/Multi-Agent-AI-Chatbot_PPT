from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multi-Agent AI Chatbot POC"
    app_env: str = "development"
    app_debug: bool = True
    app_secret_key: str = "dev-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    api_base_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"
    llm_provider: str = "openai_compatible"
    llm_model: str = "gpt-4o-mini"
    llm_base_url: str = "http://localhost:11434/v1"
    llm_api_key: str = "demo-key"
    vector_db_provider: str = "pinecone"
    pinecone_api_key: str = "demo-key"
    pinecone_environment: str = "us-east-1"
    pinecone_index_name: str = "enterprise-rag"
    database_url: str = "sqlite:///./app.db"
    upload_dir: str = "./storage/uploads"
    artifacts_dir: str = "./storage/artifacts"
    web_search_provider: str = "mock"
    serpapi_api_key: str = ""
    tesseract_cmd: str = ""
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir).resolve()

    @property
    def artifacts_path(self) -> Path:
        return Path(self.artifacts_dir).resolve()


@lru_cache
def get_settings() -> Settings:
    return Settings()
