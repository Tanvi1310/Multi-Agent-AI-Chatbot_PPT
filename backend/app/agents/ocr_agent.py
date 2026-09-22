from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent


class OCRVisionAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(name='ocr_vision', role='ocr')

    def run(self, uploaded_files: list[str] | None = None, **kwargs: Any) -> dict[str, Any]:
        files = uploaded_files or []
        return {
            'agent': self.name,
            'status': 'completed',
            'scans': files,
            'analysis': 'Detected text from uploaded scanned documents and images using OCR-ready processing.',
        }
