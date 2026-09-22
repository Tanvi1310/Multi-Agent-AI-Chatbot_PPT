from __future__ import annotations

from pathlib import Path

from app.config import get_settings


settings = get_settings()


def ensure_storage_dirs() -> None:
    Path(settings.upload_path).mkdir(parents=True, exist_ok=True)
    Path(settings.artifacts_path).mkdir(parents=True, exist_ok=True)
